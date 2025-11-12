from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import FAQForm
from .models import FAQ


def faqs(request):
    """Display all frequently asked questions."""
    items = FAQ.objects.all().order_by("id")
    return render(request, "faqs/faqs.html", {"faqs": items})


@login_required
def add_faq(request):
    """Create a new FAQ (superusers only)."""
    if not request.user.is_superuser:
        messages.error(request, "Access denied: invalid credentials.")
        return redirect("home")

    form = FAQForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "FAQ added successfully!")
            return redirect("faqs:index")
        messages.error(
            request,
            "There was an error. Please fix the form and try again.",
        )

    return render(request, "faqs/add_faq.html", {"form": form})


@login_required
def update_faq(request, id):
    """Update an existing FAQ (superusers only)."""
    if not request.user.is_superuser:
        messages.error(request, "Access denied: invalid credentials.")
        return redirect("home")

    faq = get_object_or_404(FAQ, id=id)
    form = FAQForm(request.POST or None, instance=faq)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "FAQ updated successfully!")
            return redirect("faqs:index")
        messages.error(
            request,
            "There was an error. Please fix the form and try again.",
        )

    return render(
        request, "faqs/update_faq.html", {"faq": faq, "form": form}
    )


@login_required
def delete_faq(request, id):
    """Delete an existing FAQ (superusers only)."""
    if not request.user.is_superuser:
        messages.error(request, "Access denied: invalid credentials.")
        return redirect("home")

    faq = get_object_or_404(FAQ, id=id)
    faq.delete()
    messages.success(request, "FAQ deleted successfully!")
    return redirect("faqs:index")
