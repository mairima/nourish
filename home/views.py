from django.shortcuts import render

# Create your views here.
def index(request):
    """ A view to return the index page """
    
    return render(request, 'home/index.html')

def privacy_policy(request):
    return render(request, 'terms/privacy_policy.html')

def terms_conditions(request):
    return render(request, 'terms/terms_conditions.html')