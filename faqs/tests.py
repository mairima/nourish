from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class FAQViewTests(TestCase):
    """Public FAQ page tests."""

    def test_faq_page_loads(self):
        """Public FAQ page should load successfully."""
        response = self.client.get(reverse("faqs:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "faqs/faqs.html")


class FAQAdminTests(TestCase):
    """Admin-only FAQ management page tests."""

    def setUp(self):
        # Create a SUPERUSER (required for admin FAQ views)
        self.user = User.objects.create_user(
            username="admin",
            password="pass",
            is_staff=True,
            is_superuser=True,
        )
        self.client.login(username="admin", password="pass")

    def test_add_faq_page_loads(self):
        """Add FAQ page should load for superuser."""
        response = self.client.get(reverse("faqs:add_faq"))
        self.assertEqual(response.status_code, 200)

    def test_update_faq_returns_404_if_not_found(self):
        """Update FAQ should return 404 when FAQ does not exist."""
        response = self.client.get(reverse("faqs:update_faq", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_delete_faq_returns_404_if_not_found(self):
        """Delete FAQ should return 404 when FAQ does not exist."""
        response = self.client.get(reverse("faqs:delete_faq", args=[999]))
        self.assertEqual(response.status_code, 404)
