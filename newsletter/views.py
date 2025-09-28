from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterForm


def newsletter(request):
    """Newsletter view"""
    form = NewsletterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Subscribed to newsletter!")
            return redirect("home")
        else:
            # error on submission
            messages.error(request, "ERROR, please try again.")
    template = "newsletter/newsletter.html"
    context = {
        "form": form,
    }
    return render(request, template, context)