from django.template.loader import render_to_string
from django.http import HttpResponseNotFound


def handler404(request, exception):
    """Render custom 404 page using Django template engine."""
    try:
        html = render_to_string("errors/404.html", {}, request)
        return HttpResponseNotFound(html)
    except Exception as e:
        # fallback plain text output for debugging
        return HttpResponseNotFound(f"<h1>404 - Fallback</h1><p>{e}</p>")
