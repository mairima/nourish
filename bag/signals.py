from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from bag.models import UserCartItem
from products.models import Product


@receiver(user_logged_in)
def merge_session_bag_into_user_cart(sender, user, request, **kwargs):
    """
    Merge the guest session bag into the logged-in user's DB cart.
    Prevents items disappearing on login.
    """
    session_bag = request.session.get("bag", {})

    if not session_bag:
        return

    for item_id, item_data in session_bag.items():
        try:
            product = Product.objects.get(id=int(item_id))
        except (Product.DoesNotExist, ValueError):
            continue

        # quantity stored as int or dict
        if isinstance(item_data, int):
            quantity = item_data
        else:
            quantity = item_data.get("quantity", 1)

        cart_item, created = UserCartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    # Clear session cart now that it is merged
    request.session["bag"] = {}
    request.session.modified = True


@receiver(user_logged_out)
def move_db_cart_to_session(sender, user, request, **kwargs):
    """
    When user logs out, move DB cart back into session cart.
    This keeps the cart persistent after logout.
    """
    if not user or not user.is_authenticated:
        return

    # Get items from DB
    session_bag = {}
    for item in UserCartItem.objects.filter(user=user):
        product_id = str(item.product.id)
        session_bag[product_id] = item.quantity

    # Ensure a new session key is generated (important)
    request.session.cycle_key()

    # Save DB items into the session cart
    request.session["bag"] = session_bag
    request.session.modified = True
