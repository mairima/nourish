from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product


class CheckoutPageTests(TestCase):
    def setUp(self):
        # Create product
        self.product = Product.objects.create(
            name="Test Cake",
            price=10
        )

        # Create & login user
        self.user = User.objects.create_user(
            username="tester",
            password="pass123"
        )
        self.client.login(username="tester", password="pass123")

        # Add item to session bag
        session = self.client.session
        session["bag"] = {str(self.product.id): 1}
        session.save()

    def test_checkout_page_loads(self):
        """
        Checkout should load for a logged-in user 
        who has items in their shopping bag.
        """
        url = reverse("checkout:checkout")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout.html")
