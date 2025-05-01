from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
import random, json
from .models import Category, Product, WishlistItem, CartItem, Cart, Wallet, Purchase
from django.http import JsonResponse
from decimal import Decimal
from collections import defaultdict

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            print("Form errors:", form.errors)
            messages.error(request, 'Error creating account. Please check your details.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.username.startswith('guest_'):
        message = "You're currently logged in as a guest. Create an account for a personalized experience!"
    else:
        message = "Welcome back, {}!".format(request.user.username)
    
    return render(request, 'accounts/dashboard.html', {'message' : message})

def guest_login(request):
    guest_username = f"guest_{random.randint(1000, 9999)}"
    
    guest_user = User.objects.create_user(
        username=guest_username,
        password=None
    )
    login(request, guest_user)
    messages.success(request, "You are now logged in as a guest!")
    return redirect('dashboard')

def landing_page(request):
    categories = Category.objects.all()
    random_category = random.choice(categories) if categories else None
    random_products = Product.objects.filter(category=random_category) if random_category else []

    recommended_products = []
    last_viewed_product_id = request.session.get('last_viewed_product')

    if last_viewed_product_id:
        last_product = Product.objects.filter(id=last_viewed_product_id).first()
        if last_product:
            recommended_products = Product.objects.filter(category=last_product.category).exclude(id=last_product.id)[:10]

    last_purchases = []
    recent_receipts = []

    if request.user.is_authenticated:
        purchases = Purchase.objects.filter(user=request.user).order_by('-timestamp')[:50]
        last_purchases = [p.product for p in purchases[:10]]

        grouped_purchases = defaultdict(list)
        for purchase in purchases:
            grouped_purchases[purchase.timestamp].append(purchase)

        for i, (timestamp, items) in enumerate(grouped_purchases.items()):
            if i >= 10:
                break
            item_names = ', '.join([item.product.name for item in items])
            total_price = sum(item.product.price * item.quantity for item in items)
            recent_receipts.append({
                'items': items,
                'total': total_price
            })

    context = {
        'random_category': random_category,
        'random_products': random_products,
        'recommended_products': recommended_products,
        'last_purchases': last_purchases,
        'recent_receipts': recent_receipts,
    }
    return render(request, 'accounts/landing_page.html', context)

def faq(request):
    return render(request, 'accounts/faq.html')

def category_page(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'accounts/category_page.html', {'category': category, 'products': products})

@login_required
def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'accounts/wishlist.html', {'wishlist': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, product_id):
    WishlistItem.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('wishlist')

@login_required
def move_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.filter(user=request.user, product=product).delete()
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'accounts/cart.html', {'cart': cart_items})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('cart')



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.session['last_viewed_product'] = product.id
    return render(request, 'accounts/product_detail.html', {'product': product})

def search_products(request):
    query = request.GET.get('q', '') 
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'accounts/search_results.html', {'query': query, 'results': results})

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'accounts/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'user': request.user
    })

@login_required
def process_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            total_price = Decimal(str(data.get("total_price")))

            user = request.user

            if user.wallet.balance >= total_price:
                user.wallet.balance -= total_price
                user.wallet.save()
                cart_items = CartItem.objects.filter(user=user)
                for item in cart_items:
                    Purchase.objects.create(
                        user=user,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )
                
                cart_items.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Insufficient funds.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request.'})

@login_required
def thank_you(request):
    return render(request, 'accounts/thank_you.html')

@login_required
def history(request):
    purchases = Purchase.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'accounts/history.html', {
        'purchases': purchases
    })

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect('forgot_password')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('forgot_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(password1)
            user.save()
            messages.success(request, "Password successfully reset. You can now log in.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Username not found.")
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')