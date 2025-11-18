from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """Render the bag contents page."""
    return render(request, "bag/bag.html")


from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Product
from bag.models import UserCartItem


def add_to_bag(request, item_id):
    """Add a quantity of a product to the shopping bag (persistent for logged-in users)."""
    product = get_object_or_404(Product, pk=item_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    redirect_url = (
        request.POST.get("redirect_url")
        or reverse("products:products_index")
    )

    # Update SESSION bag first
    bag = request.session.get("bag", {})
    item_key = str(item_id)

    new_qty = bag.get(item_key, 0) + quantity
    bag[item_key] = new_qty
    request.session["bag"] = bag

    # Save to DB for logged-in users

    if request.user.is_authenticated:
        cart_item, _ = UserCartItem.objects.get_or_create(
            user=request.user,
            product=product
        )
        cart_item.quantity = new_qty
        cart_item.save()

    # Messages
    if new_qty > quantity:
        messages.success(
            request, f"Updated {product.name} quantity to {new_qty}."
        )
    else:
        messages.success(request, f"Added {product.name} to your bag.")

    return redirect(redirect_url)



def adjust_bag(request, item_id):
    """Set the quantity for a product (persistent for logged-in users)."""
    product = get_object_or_404(Product, pk=item_id)

    try:
        quantity = int(request.POST.get("quantity", 0))
    except (TypeError, ValueError):
        quantity = 0

    bag = request.session.get("bag", {})
    item_key = str(item_id)

    if quantity > 0:
        bag[item_key] = quantity
        messages.success(
            request,
            f"Updated {product.name} quantity to {quantity}"
        )
    else:
        if item_key in bag:
            bag.pop(item_key, None)
            messages.success(
                request,
                f"Removed {product.name} from your bag"
            )
        else:
            messages.info(request, f"{product.name} was not in your bag")

    request.session["bag"] = bag

    # --- DB Persistence ---
    if request.user.is_authenticated:
        try:
            if quantity > 0:
                item = UserCartItem.objects.get(
                    user=request.user,
                    product=product
                )
                item.quantity = quantity
                item.save()
            else:
                UserCartItem.objects.filter(
                    user=request.user,
                    product=product
                ).delete()
        except UserCartItem.DoesNotExist:
            pass

    return redirect(reverse("view_bag"))


def remove_from_bag(request, item_id):
    """Remove a product from the bag (persistent for logged-in users)."""
    product = get_object_or_404(Product, pk=item_id)
    bag = request.session.get("bag", {})
    item_key = str(item_id)

    try:
        if item_key in bag:
            bag.pop(item_key, None)
            request.session["bag"] = bag
            messages.success(
                request,
                f"Removed {product.name} from your bag"
            )
        else:
            messages.info(request, f"{product.name} was not in your bag")

        # --- DB Persistence ---
        if request.user.is_authenticated:
            UserCartItem.objects.filter(
                user=request.user,
                product=product
            ).delete()

        return HttpResponse(status=200)

    except Exception as err:
        messages.error(request, f"Error removing item: {err}")
        return HttpResponse(status=500)
