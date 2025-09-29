from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FAQForm
from .models import FAQ


def faqs(request):
    """FAQs page to list all FAQs"""
    faqs = FAQ.objects.all()
    template = "faqs/faqs.html"
    context = {
        "faqs": faqs,
    }
    return render(request, template, context)


@login_required
def add_faq(request):
    """Create a new FAQ (superusers only)."""
    if not request.user.is_superuser:
        messages.error(request, "Access Denied: Invalid Credentials.")
        return redirect("home")

    form = FAQForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "FAQ added successfully!")
            return redirect("faqs")
        else:
            # error on submission
            messages.error(request, "ERROR, please try again.")

    template = "faqs/add_faq.html"
    context = {
        "form": form,
    }
    return render(request, template, context)


@login_required
def update_faq(request, id):
    """Update an existing FAQ (superusers only)."""
    if not request.user.is_superuser:
        messages.error(request, "Access Denied: Invalid Credentials.")
        return redirect("home")

    faq = get_object_or_404(FAQ, id=id)
    form = FAQForm(request.POST or None, instance=faq)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "FAQ updated successfully!")
            return redirect("faqs")
        else:
            # error on submission
            messages.error(request, "ERROR, please try again.")

    template = "faqs/update_faq.html"
    context = {
        "faq": faq,
        "form": form,
    }
    return render(request, template, context)


@login_required
def delete_faq(request, id):
    """Delete an existing FAQ (superusers only)."""
    if not request.user.is_superuser:
        messages.error(request, "Access Denied: Invalid Credentials.")
        return redirect("home")

    faq = get_object_or_404(FAQ, id=id)
    faq.delete()
    messages.success(request, "FAQ updated successfully!")
    return redirect("faqs:index")
