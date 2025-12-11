"""Tests for the home page view."""

from django.test import TestCase
from django.urls import reverse


class HomeTests(TestCase):
    """Test suite for the home page."""

    def test_home_page_loads(self):
        """Ensure the home page loads and uses the correct template."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
