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


from django.http import HttpResponseNotFound
from django.shortcuts import render


from django.shortcuts import render
from django.http import HttpResponseNotFound

def error_404_view(request, exception=None):
    """Render custom 404 or fallback text if template fails."""
    try:
        print("📄 Trying to load template: errors/404.html")
        response = render(request, "errors/404.html", status=404)
        print("✅ 404 template loaded successfully")
        return response
    except Exception as e:
        print("❌ ERROR in 404 view:", e)
        return HttpResponseNotFound(
            f"<h1>404 - Page Not Found</h1><p>Error: {e}</p>"
        )
