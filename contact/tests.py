
# Create your tests here.
from django.test import TestCase
from contact.forms import ContactForm


class ContactFormTests(TestCase):
    def test_contact_form_valid(self):
        form = ContactForm({
            "name": "Mairi",
            "email": "mairi@example.com",
            "subject": "Test",
            "message": "Hello"
        })
        self.assertTrue(form.is_valid())
