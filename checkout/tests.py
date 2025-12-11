from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product


class CheckoutPageTests(TestCase):
    """Tests for the checkout page behavior."""

    def setUp(self):
        """Create a test user, product, and session bag."""
        self.product = Product.objects.create(
            name="Test Cake",
            price=10
        )

        self.user = User.objects.create_user(
            username="tester",
            password="pass123"
        )
        self.client.login(
            username="tester",
            password="pass123"
        )

        session = self.client.session
        session["bag"] = {str(self.product.id): 1}
        session.save()

    def test_checkout_page_loads(self):
        """
        Ensure checkout page loads for an authenticated user
        with items in the shopping bag.
        """
        url = reverse("checkout:checkout")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout.html")
