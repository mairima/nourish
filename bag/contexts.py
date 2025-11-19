from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """Build cart context from the session bag."""
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get("bag", {})

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=int(item_id))

        if isinstance(item_data, int):
            quantity = item_data
            total += quantity * product.price
            product_count += quantity

            bag_items.append({
                "item_id": item_id,
                "quantity": quantity,
                "product": product,
            })

        else:
            # For sites using size variants (you can keep it—it won’t break anything)
            for size, quantity in item_data.get("items_by_size", {}).items():
                total += quantity * product.price
                product_count += quantity

                bag_items.append({
                    "item_id": item_id,
                    "quantity": quantity,
                    "product": product,
                    "size": size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(
            settings.STANDARD_DELIVERY_PERCENTAGE / 100
        )
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = Decimal("0.00")
        free_delivery_delta = Decimal("0.00")

    grand_total = delivery + total

    return {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "grand_total": grand_total,
    }
