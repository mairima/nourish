from django.shortcuts import redirect
from django.http import HttpResponse

def home(request):
    if not request.user.is_authenticated:
        return redirect('account_login')  # avoids loop when logged out
    return HttpResponse(f"Welcome, {request.user.get_username()} 👋")
