from django.db import models


class Contact(models.Model):
    """Contact model for users to contact admin"""
    name = models.CharField(max_length=75, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name