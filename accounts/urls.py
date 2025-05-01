from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import add_to_cart, add_to_wishlist, product_detail, search_products, process_payment

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('guest-login/', views.guest_login, name='guest_login'),
    path('landing/', views.landing_page, name='landing'),
    path('faq/', views.faq, name='faq'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/move_to_cart/<int:product_id>/', views.move_to_cart, name='move_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('category/<int:category_id>/', views.category_page, name='category_page'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('search_results/', search_products, name='search_products'),
    path('checkout/', views.checkout, name='checkout'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('history/', views.history, name='history'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)