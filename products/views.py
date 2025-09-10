from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.paginator import Paginator
from .models import Product, Category


def all_products(request):
    """List products with search, category filter, sorting, and pagination."""
    qs = Product.objects.select_related('category').all()

    # Params
    query = (request.GET.get('q') or '').strip()
    sort = request.GET.get('sort')                      # price | rating | name | category
    direction = request.GET.get('direction', 'asc')     # asc | desc
    category_param = request.GET.get('category')        # e.g. "Cakes,Drinks"

    # Sorting (safe map)
    allowed_sorts = {
        'price': 'price',
        'rating': 'rating',
        'name': 'name',
        'category': 'category__name',
    }
    if sort in allowed_sorts:
        sortkey = allowed_sorts[sort]
        if sort == 'name':
            qs = qs.annotate(lower_name=Lower('name'))
            sortkey = 'lower_name'
        if direction == 'desc':
            sortkey = f'-{sortkey}'
        qs = qs.order_by(sortkey)

    # Category filter
    current_categories = None
    if category_param:
        names = [c.strip() for c in category_param.split(',') if c.strip()]
        if names:
            qs = qs.filter(category__name__in=names)
            current_categories = Category.objects.filter(name__in=names)

    # Search
    if 'q' in request.GET and not query:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('products:products_index'))
    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Pagination
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'search_term': query,
        'current_categories': current_categories,
        'current_sort': sort,
        'current_direction': 'desc' if direction == 'desc' else 'asc',
        'all_categories': Category.objects.order_by('friendly_name', 'name'),
        'selected_category_raw': category_param or '',
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """Show individual product details."""
    product = get_object_or_404(
        Product.objects.select_related('category'),
        pk=product_id
    )
    return render(request, 'products/products_detail.html', {'product': product})
