from django.shortcuts import (render, redirect, reverse,
                              HttpResponse, get_object_or_404)
from django.contrib import messages

from products.models import Product


def view_bag(request):
    """Render the bag contents page."""
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag (no sizes)."""
    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', reverse('products:products_index'))

    bag = request.session.get('bag', {})
    item_key = str(item_id)

    previous_qty = bag.get(item_key, 0)
    bag[item_key] = previous_qty + quantity

    request.session['bag'] = bag

    if previous_qty:
        messages.success(request, f'Updated {product.name} quantity to {bag[item_key]}')
    else:
        messages.success(request, f'Added {product.name} to your bag')

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Set the quantity for a product (no sizes)."""
    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity', 0))
    bag = request.session.get('bag', {})
    item_key = str(item_id)

    if quantity > 0:
        bag[item_key] = quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_key]}')
    else:
        bag.pop(item_key, None)
        messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the product from the shopping bag (no sizes)."""
    product = get_object_or_404(Product, pk=item_id)
    item_key = str(item_id)

    try:
        bag = request.session.get('bag', {})
        bag.pop(item_key, None)
        request.session['bag'] = bag
        messages.success(request, f'Removed {product.name} from your bag')
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
