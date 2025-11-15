from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.paginator import Paginator
from .models import Product, Category
from .forms import ProductForm


# Display all products
def all_products(request):
    qs = Product.objects.select_related("category").all()
    query = (request.GET.get("q") or "").strip()
    sort = request.GET.get("sort")
    direction = "desc" if request.GET.get("direction") == "desc" else "asc"
    category_param = request.GET.get("category")

    if sort:
        sortkey = None
        if sort == "name":
            qs = qs.annotate(lower_name=Lower("name"))
            sortkey = "lower_name"
        elif sort == "category":
            sortkey = "category__name"
        elif sort in {"price", "rating"}:
            sortkey = sort

        if sortkey:
            if direction == "desc":
                sortkey = f"-{sortkey}"
            qs = qs.order_by(sortkey)

    current_categories = None
    if category_param:
        names = [c.strip() for c in category_param.split(",") if c.strip()]
        if names:
            qs = qs.filter(category__name__in=names)
            current_categories = Category.objects.filter(name__in=names)

    if query:
        qs = qs.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if not qs.ordered:
        qs = qs.order_by("pk")

    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "products": page_obj,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "search_term": query,
        "current_categories": current_categories,
        "current_sort": sort,
        "current_direction": direction,
        "current_sorting": f"{sort}_{direction}" if sort else "None_None",
        "all_categories": Category.objects.order_by("friendly_name", "name"),
        "selected_category_raw": category_param or "",
    }
    return render(request, "products/products.html", context)


# Display product details (UPDATED)
def product_detail(request, product_id):
    try:
        product = (
            Product.objects.select_related("category")
            .get(pk=product_id)
        )
    except Product.DoesNotExist:
        messages.error(request, "This product no longer exists.")
        return redirect(reverse("products:products"))

    return render(
        request,
        "products/product_detail.html",
        {"product": product},
    )


# Add a new product (superuser only)
@login_required
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Successfully added product!")
            return redirect(
                reverse("products:product_detail", args=[product.id])
            )
        messages.error(
            request,
            "Failed to add product. Please ensure the form is valid.",
        )
    else:
        form = ProductForm()

    return render(request, "products/add_product.html", {"form": form})


# Edit an existing product (superuser only)
@login_required
def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated product!")
            return redirect(
                reverse("products:product_detail", args=[product.id])
            )
        messages.error(
            request,
            "Failed to update product. Please ensure the form is valid.",
        )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f"You are editing {product.name}")

    return render(
        request,
        "products/includes/edit_product.html",
        {"form": form, "product": product},
    )


# Delete a product (superuser only) — UPDATED
@login_required
def delete_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)
    product_id_str = str(product_id)

    # Remove product from the bag if it exists
    bag = request.session.get("bag", {})
    if product_id_str in bag:
        bag.pop(product_id_str)
        request.session["bag"] = bag
        messages.info(
            request,
            "This product was also removed from your bag."
        )

    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect(reverse("products:products"))
