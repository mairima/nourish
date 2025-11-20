from django.test import TestCase


class RootURLTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_products_include(self):
        response = self.client.get("/products/")
        self.assertIn(response.status_code, [200, 302])

    def test_bag_include(self):
        response = self.client.get("/bag/")
        self.assertIn(response.status_code, [200, 302])

    def test_checkout_include(self):
        response = self.client.get("/checkout/")
        self.assertIn(response.status_code, [200, 302])

    def test_profiles_include(self):
        response = self.client.get("/profiles/")
        self.assertIn(response.status_code, [200, 302])

    def test_contact_include(self):
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)

    def test_faqs_include(self):
        response = self.client.get("/faqs/")
        self.assertEqual(response.status_code, 200)

    def test_newsletter_include(self):
        response = self.client.get("/newsletter/")
        self.assertEqual(response.status_code, 200)

    def test_sitemap(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
