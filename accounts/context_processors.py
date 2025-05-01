from collections import defaultdict
from .models import Purchase

def recent_receipts_processor(request):
    recent_receipts = []

    if request.user.is_authenticated:
        purchases = Purchase.objects.filter(user=request.user).order_by('-timestamp')[:50]

        grouped_purchases = defaultdict(list)
        for purchase in purchases:
            grouped_purchases[purchase.timestamp].append(purchase)

        for i, (timestamp, items) in enumerate(grouped_purchases.items()):
            if i >= 10:
                break
            total_price = sum(item.product.price * item.quantity for item in items)
            recent_receipts.append({
                'items': items,
                'total': total_price
            })

    return {'recent_receipts': recent_receipts}
