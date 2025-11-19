from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
    reverse,
    HttpResponse,
)
from products.models import Product
from bag.models import UserCartItem


def view_bag(request):
    """Render the bag contents page."""
    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """Add quantity of an item to the bag with DB/session sync."""
    product = get_object_or_404(Product, pk=item_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    redirect_url = (
        request.POST.get("redirect_url")
        or reverse("products:products")
    )

    # --- Update session bag ---
    bag = request.session.get("bag", {})
    item_key = str(item_id)

    old_qty = bag.get(item_key, 0)
    new_qty = old_qty + quantity
    bag[item_key] = new_qty
    request.session["bag"] = bag

    # --- Update DB cart (persistent cart) ---
    if request.user.is_authenticated:
        cart_item, _ = UserCartItem.objects.get_or_create(
            user=request.user,
            product=product,
        )
        cart_item.quantity = new_qty   # sync with session, no double counting
        cart_item.save()

    # --- Messages ---
    if old_qty > 0:
        messages.success(
            request,
            f"Updated {product.name} quantity to {new_qty}.",
        )
    else:
        messages.success(
            request,
            f"Added {product.name} to your bag.",
        )

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust quantity of a selected item (session + DB)."""
    product = get_object_or_404(Product, pk=item_id)

    try:
        quantity = int(request.POST.get("quantity", 0))
    except (TypeError, ValueError):
        quantity = 0

    bag = request.session.get("bag", {})
    item_key = str(item_id)

    # --- Update session ---
    if quantity > 0:
        bag[item_key] = quantity
        messages.success(
            request,
            f"Updated {product.name} quantity to {quantity}.",
        )
    else:
        bag.pop(item_key, None)
        messages.success(
            request,
            f"Removed {product.name} from your bag.",
        )

    request.session["bag"] = bag

    # --- Sync DB cart ---
    if request.user.is_authenticated:
        if quantity > 0:
            cart_item, _ = UserCartItem.objects.get_or_create(
                user=request.user,
                product=product,
            )
            cart_item.quantity = quantity
            cart_item.save()
        else:
            UserCartItem.objects.filter(
                user=request.user,
                product=product,
            ).delete()

    return redirect(reverse("bag:view_bag"))


def remove_from_bag(request, item_id):
    """Remove item fully from bag (session + DB)."""
    product = get_object_or_404(Product, pk=item_id)

    bag = request.session.get("bag", {})
    item_key = str(item_id)

    # --- Remove from session ---
    if item_key in bag:
        bag.pop(item_key, None)
        request.session["bag"] = bag
        messages.success(
            request,
            f"Removed {product.name} from your bag.",
        )

    # --- Remove from DB cart ---
    if request.user.is_authenticated:
        UserCartItem.objects.filter(
            user=request.user,
            product=product,
        ).delete()

    return HttpResponse(status=200)
