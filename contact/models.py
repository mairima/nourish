from django.db import models


class Contact(models.Model):
    """Model for user contact messages sent to the admin."""
    name = models.CharField(max_length=75, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the contact name as string representation."""
        return self.name
