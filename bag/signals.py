from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserCartItem


@receiver(user_logged_in)
def load_cart_after_login(sender, user, request, **kwargs):
    session_bag = request.session.get('bag', {})

    # Add DB items to session bag
    for item in UserCartItem.objects.filter(user=user):
        product_id = str(item.product.id)
        session_bag[product_id] = item.quantity

    request.session['bag'] = session_bag
