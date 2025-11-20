from django.test import TestCase
from django.urls import reverse
from products.models import Product


class BagTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Cake", price=10)

    def test_view_bag(self):
        response = self.client.get(reverse("bag:view_bag"))
        self.assertEqual(response.status_code, 200)

    def test_add_to_bag(self):
        response = self.client.post(
            reverse("bag:add_to_bag", args=[self.product.id]),
            {"quantity": 1}
        )
        session = self.client.session
        self.assertIn(str(self.product.id), session["bag"])

    def test_adjust_bag(self):
        session = self.client.session
        session["bag"] = {str(self.product.id): 1}
        session.save()

        self.client.post(
            reverse("bag:adjust_bag", args=[self.product.id]),
            {"quantity": 3}
        )
        self.assertEqual(self.client.session["bag"][str(self.product.id)], 3)

    def test_remove_from_bag(self):
        session = self.client.session
        session["bag"] = {str(self.product.id): 1}
        session.save()

        self.client.post(reverse("bag:remove_from_bag", args=[self.product.id]))
        self.assertNotIn(str(self.product.id), self.client.session["bag"])
