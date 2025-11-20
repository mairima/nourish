from django.db import models
from django.urls import reverse
from django.templatetags.static import static
from cloudinary.models import CloudinaryField


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(
        max_length=254, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name or self.name


class Product(models.Model):
    category = models.ForeignKey(
        "Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    rating = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )
    image_filename = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    image_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
    )
    image = CloudinaryField("image", null=True, blank=True)

    def __str__(self):
        return self.name

    # 🚀 Added for sitemap + SEO
    def get_absolute_url(self):
        """
        Return the canonical product detail URL.
        Used by Django's sitemap framework.
        """
        return reverse("products:product_detail", args=[self.pk])

    @property
    def image_url_fixed(self):
        """
        Returns best possible image source:

        1. CloudinaryField upload
        2. Old Cloudinary URL (png→jpg fallback)
        3. Static filename
        4. Default image
        """
        # CloudinaryField upload
        if (
            self.image
            and hasattr(self.image, "url")
            and self.image.url
            and "placeholder" not in self.image.url
            and not self.image.url.endswith(
                "/image/upload/placeholder"
            )
        ):
            return self.image.url

        # Old Cloudinary URL fallback
        if self.image_url:
            url = self.image_url
            if url.endswith(".png"):
                return f"{url[:-4]}.jpg"
            return url

        # Static file fallback
        if self.image_filename:
            return static(f"images/{self.image_filename}")

        # Default image
        return static("images/noimage.png")
