from django.http import HttpResponse
from django.shortcuts import render


# Home view
def index(request):
    return HttpResponse("Products home")


# 404 handler
def handler404(request, exception):
    return render(request, "errors/404.html", status=404)
