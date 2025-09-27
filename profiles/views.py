from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# do NOT import UserProfile at module import time — import inside the view to avoid
# circular/import-time problems that can prevent Django registering URL names.
try:
    from .forms import ProfileForm
except Exception:
    ProfileForm = None


@login_required
def profile(request):
    """
    Display the user's profile and ensure it exists.
    """
    from .models import UserProfile
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "profiles/profile.html", {"profile": profile})


@login_required
def profile_edit(request):
    """
    Edit the user's profile using a ModelForm (ProfileForm).
    If ProfileForm is missing, show a message and redirect back.
    """
    from .models import UserProfile
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if ProfileForm is None:
        messages.error(request, "Profile editing is not available (ProfileForm missing).")
        return redirect("profile")

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profiles/profile_edit.html", {"form": form})
