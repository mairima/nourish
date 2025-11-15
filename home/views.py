from django.http import HttpResponseNotFound
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


def error_404_view(request, exception=None):
    """Render custom 404 page or fallback text on error."""
    try:
        return render(request, "errors/404.html", status=404)
    except Exception as error:
        return HttpResponseNotFound(
            "<h1>404 - Page Not Found</h1>"
            f"<p>Error: {error}</p>"
        )
