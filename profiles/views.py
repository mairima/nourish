# profiles/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import UserProfile
from .forms import ProfileForm
from checkout.models import Order


@login_required
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)

    # Email (fallback via allauth if User.email is empty)
    user_email = request.user.email
    if not user_email:
        try:
            from allauth.account.models import EmailAddress
            user_email = EmailAddress.objects.filter(
                user=request.user, primary=True
            ).values_list("email", flat=True).first()
        except Exception:
            user_email = None

    # Orders linked via FK first
    orders = profile.orders.all().order_by("-date")

    # Fallback: also show guest orders that match the same email
    if not orders.exists() and user_email:
        orders = Order.objects.filter(email__iexact=user_email).order_by("-date")

    context = {
        "profile": profile,
        "form": form,
        "orders": orders,
        "user_email": user_email,
        "on_profile_page": True,
    }
    return render(request, "profiles/profile.html", context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))
    return render(request, "checkout/checkout:checkout_success.html", {
        "order": order,
        "from_profile": True,
    })


@login_required
def profile_edit(request):
    return render(request, "profiles/profile_edit.html", {})

# Optional alias
profile_edit_alias = profile
