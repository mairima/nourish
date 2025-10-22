# products/views.py
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.paginator import Paginator
from .models import Product, Category
from .forms import ProductForm



def all_products(request):
    """List products with search, category filter, sorting, and pagination."""
    qs = Product.objects.select_related('category').all()

    # Params from query string
    query = (request.GET.get('q') or '').strip()
    sort = request.GET.get('sort')                           # 'price' | 'rating' | 'name' | 'category'
    direction = 'desc' if request.GET.get('direction') == 'desc' else 'asc'
    category_param = request.GET.get('category')             # e.g. "Cakes,Drinks"

    # ---- Sorting (case-insensitive name; category sorts by category name) ----
    if sort:
        sortkey = None
        if sort == 'name':
            qs = qs.annotate(lower_name=Lower('name'))
            sortkey = 'lower_name'
        elif sort == 'category':
            sortkey = 'category__name'
        elif sort in {'price', 'rating'}:
            sortkey = sort

        if sortkey:
            if direction == 'desc':
                sortkey = f'-{sortkey}'
            qs = qs.order_by(sortkey)

    # ---- Category filter ----
    current_categories = None
    if category_param:
        names = [c.strip() for c in category_param.split(',') if c.strip()]
        if names:
            qs = qs.filter(category__name__in=names)
            current_categories = Category.objects.filter(name__in=names)

    # ---- Search (ignore empty q so sorting stays intact) ----
    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # ---- Stable fallback ordering to avoid UnorderedObjectListWarning ----
    if not qs.ordered:
        qs = qs.order_by('pk')

    # ---- Pagination ----
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'products': page_obj,                        # iterate over this in template
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'search_term': query,
        'current_categories': current_categories,
        'current_sort': sort,
        'current_direction': direction,
        'current_sorting': f'{sort}_{direction}' if sort else 'None_None',
        'all_categories': Category.objects.order_by('friendly_name', 'name'),
        'selected_category_raw': category_param or '',
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """Show individual product details."""
    product = get_object_or_404(Product.objects.select_related('category'), pk=product_id)
    return render(request, 'products/products_detail.html', {'product': product})

def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)