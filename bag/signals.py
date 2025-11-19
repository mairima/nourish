from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from bag.models import UserCartItem
from products.models import Product


@receiver(user_logged_in)
def merge_session_bag_into_user_cart(sender, request, user, **kwargs):
    """
    When the user logs in:
    1. Merge the guest session bag into the user's DB cart.
    2. Restore the entire DB cart back into the session.
    This prevents losing the cart during login (desktop & mobile).
    """
    session_bag = request.session.get("bag", {})

    # ---- Merge session bag into DB cart ----
    for item_id, item_data in session_bag.items():
        try:
            product = Product.objects.get(id=int(item_id))
        except (Product.DoesNotExist, ValueError):
            continue

        if isinstance(item_data, int):
            quantity = item_data
        else:
            # Safety if some carts stored dicts
            quantity = item_data.get("quantity", 1)

        cart_item, created = UserCartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    # ---- Restore DB cart back into session ----
    restored = {}
    for item in UserCartItem.objects.filter(user=user):
        restored[str(item.product.id)] = item.quantity

    request.session["bag"] = restored
    request.session.modified = True
