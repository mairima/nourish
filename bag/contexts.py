from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """Build cart context dictionary from the session bag."""
    bag_items = []
    total = Decimal("0.00")
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
            sizes = item_data.get("items_by_size", {})
            for size, quantity in sizes.items():
                total += quantity * product.price
                product_count += quantity

                bag_items.append({
                    "item_id": item_id,
                    "quantity": quantity,
                    "product": product,
                    "size": size,
                })

    threshold = settings.FREE_DELIVERY_THRESHOLD
    percentage = settings.STANDARD_DELIVERY_PERCENTAGE

    if total < threshold:
        delivery = total * Decimal(percentage / 100)
        free_delivery_delta = threshold - total
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
        "free_delivery_threshold": threshold,
        "grand_total": grand_total,
    }
