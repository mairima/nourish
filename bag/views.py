# bag/views.py
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST

from products.models import Product


def view_bag(request):
    """Render the bag contents page (no sizes)."""
    return render(request, 'bag/bag.html')


@require_POST
def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag (no sizes)."""
    product = get_object_or_404(Product, pk=item_id)

    # Safe quantity parse
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    redirect_url = request.POST.get('redirect_url') or reverse('products:products_index')

    bag = request.session.get('bag', {})
    key = str(item_id)

    previous_qty = bag.get(key, 0)
    bag[key] = previous_qty + max(quantity, 0)
    request.session['bag'] = bag

    if previous_qty:
        messages.success(request, f'Updated {product.name} quantity to {bag[key]}')
    else:
        messages.success(request, f'Added {product.name} to your bag')

    return redirect(redirect_url)


@require_POST
def adjust_bag(request, item_id):
    """Set the quantity for a product (no sizes)."""
    product = get_object_or_404(Product, pk=item_id)

    # Safe quantity parse
    try:
        quantity = int(request.POST.get('quantity', 0))
    except (TypeError, ValueError):
        quantity = 0

    bag = request.session.get('bag', {})
    key = str(item_id)

    if quantity > 0:
        bag[key] = quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[key]}')
    else:
        if key in bag:
            bag.pop(key)
            messages.success(request, f'Removed {product.name} from your bag')
        else:
            messages.error(request, f'{product.name} was not in your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


@require_POST
def remove_from_bag(request, item_id):
    """Remove the product from the shopping bag (no sizes)."""
    product = get_object_or_404(Product, pk=item_id)
    bag = request.session.get('bag', {})
    key = str(item_id)

    if key in bag:
        bag.pop(key)
        request.session['bag'] = bag
        messages.success(request, f'Removed {product.name} from your bag')
    else:
        messages.error(request, f'{product.name} was not in your bag')

    # AJAX-friendly response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponse(status=200)
    return redirect(reverse('view_bag'))
