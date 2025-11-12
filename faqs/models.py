from django.db import models


class FAQ(models.Model):
    """Model representing a frequently asked question."""
    question = models.CharField(max_length=100, null=False, blank=False)
    answer = models.TextField(null=False, blank=False)

    def __str__(self):
        """Return the question text as string representation."""
        return self.question
