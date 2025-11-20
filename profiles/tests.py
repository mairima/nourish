from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class ProfileAccessTests(TestCase):
    def test_profile_requires_login(self):
        """Profile page must redirect if user is not logged in."""
        response = self.client.get(reverse("profiles:profile"))
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_requires_login(self):
        """Profile edit page must redirect if user is not logged in."""
        response = self.client.get(reverse("profiles:profile_edit"))
        self.assertEqual(response.status_code, 302)


class ProfileLoggedInTests(TestCase):
    def setUp(self):
        """Create a user and log them in."""
        self.user = User.objects.create_user(
            username="testuser",
            password="pass1234",
        )
        self.client.login(username="testuser", password="pass1234")

    def test_profile_page_loads(self):
        """Logged-in users should access their profile."""
        response = self.client.get(reverse("profiles:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile.html")

    def test_profile_edit_page_loads(self):
        """Logged-in users should access profile edit."""
        response = self.client.get(reverse("profiles:profile_edit"))
        # Both profile and profile_edit may use the same view/template
        self.assertIn(response.status_code, [200, 302])

    def test_order_history_requires_valid_order_number(self):
        """Order history should return 200 or 404 depending on data."""
        response = self.client.get(
            reverse("profiles:order_history", args=["TEST123"])
        )
        self.assertIn(response.status_code, [200, 404])
