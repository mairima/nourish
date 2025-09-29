from django.db import models


class FAQ(models.Model):
    """FAQs model: Frequently Asked Questions"""
    question = models.CharField(max_length=100, null=False, blank=False)
    answer = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.question