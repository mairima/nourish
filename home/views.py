from django.shortcuts import render


def index(request):
    """Return the home page."""
    return render(request, "home/index.html")


def privacy_policy(request):
    """Return the privacy policy page."""
    return render(request, "terms/privacy_policy.html")


def terms_conditions(request):
    """Return the terms and conditions page."""
    return render(request, "terms/terms_conditions.html")
