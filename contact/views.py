from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def contact(request):
    """Contact view"""
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully!")
            return redirect("home")
        else:
            # error on submission
            messages.error(request, "ERROR, please try again.")
    template = "contact/contact.html"
    context = {
        "form": form,
    }
    return render(request, template, context)