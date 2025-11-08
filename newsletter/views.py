from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_welcome_email(email):
    subject = "Welcome to Nourish Bakery 🍰"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [email]
    html_content = render_to_string('newsletter/welcome_email.html', {})
    msg = EmailMultiAlternatives(subject, '', from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def newsletter(request):
    """Handle newsletter subscription form and send welcome email."""
    form = NewsletterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            # Save subscriber
            subscription = form.save()

            # Send the welcome email right after saving
            send_welcome_email(subscription.email)

            messages.success(
                request,
                "You're subscribed! A welcome email with your discount code "
                "has been sent."
            )
            return redirect("home")
        else:
            messages.error(request, "Error: please check your email and try again.")

    template = "newsletter/newsletter.html"
    context = {"form": form}
    return render(request, template, context)

def unsubscribe(request, token):
    """Deactivate newsletter subscription via token link."""
    subscription = get_object_or_404(
        NewsletterSubscription, unsubscribe_token=token
    )
    if subscription.is_active:
        subscription.is_active = False
        subscription.save()
        messages.success(
            request, "You have successfully unsubscribed from our newsletter."
        )
    else:
        messages.info(request, "You were already unsubscribed.")
    return render(request, "newsletter/unsubscribed.html")
