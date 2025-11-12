from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import NewsletterSubscription
from .forms import NewsletterForm


def send_welcome_email(email):
    """Send a rich HTML welcome email."""
    subject = "Welcome to Nourish Bakery 🍰"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [email]
    html_content = render_to_string("newsletter/welcome_email.html", {})
    msg = EmailMultiAlternatives(subject, "", from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def newsletter(request):
    """Handle newsletter signup form."""
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            subscription, _ = NewsletterSubscription.objects.get_or_create(
                email=email
            )

            # Reactivate if previously unsubscribed
            if not subscription.is_active:
                subscription.is_active = True
                subscription.save()

            # Build unsubscribe link
            unsubscribe_link = request.build_absolute_uri(
                reverse(
                    "newsletter:unsubscribe",
                    args=[subscription.unsubscribe_token],
                )
            )

            # Build welcome message
            subject = "Welcome to Nourish Newsletter!"
            message = (
                "Hello!\n\n"
                "Thank you for subscribing to Nourish Bakery 💕\n"
                "You’ll now receive updates, new desserts, "
                "and exclusive offers.\n\n"
                f"As a warm welcome, here’s your 10% discount code:\n"
                f"👉 {subscription.discount_code}\n\n"
                "Use it on your next order before "
                f"{subscription.discount_expires.strftime('%B %d, %Y')}.\n\n"
                f"If you ever wish to unsubscribe, click here:\n"
                f"{unsubscribe_link}\n\n"
                "With love,\n"
                "The Nourish Cakes & Snacks Team"
            )

            # Send confirmation email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )

            messages.success(
                request,
                "Thank you for subscribing! A confirmation email was sent.",
            )
            return redirect("newsletter:newsletter")
    else:
        form = NewsletterForm()

    return render(request, "newsletter/newsletter.html", {"form": form})


def unsubscribe(request, token):
    """Handle newsletter unsubscription securely."""
    try:
        subscription = NewsletterSubscription.objects.get(
            unsubscribe_token=token
        )
        if subscription.is_active:
            subscription.is_active = False
            subscription.save()
            messages.success(
                request,
                "You have been unsubscribed from the Nourish newsletter.",
            )
        else:
            messages.info(request, "You are already unsubscribed.")
    except NewsletterSubscription.DoesNotExist:
        messages.error(request, "Invalid unsubscribe link.")
    return redirect("home")
