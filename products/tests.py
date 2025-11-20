
# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category


class ProductModelTests(TestCase):
    def test_product_str(self):
        product = Product.objects.create(name="Juice", price=3)
        self.assertEqual(str(product), "Juice")

    def test_category_str(self):
        cat = Category.objects.create(name="drinks")
        self.assertEqual(str(cat), "drinks")


class ProductViewTests(TestCase):
    def test_product_list_page(self):
        response = self.client.get(reverse("products:products"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")

    def test_product_detail_page(self):
        product = Product.objects.create(name="Cake", price=5)
        response = self.client.get(
            reverse("products:product_detail", args=[product.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")
