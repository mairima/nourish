# products/models.py
from django.db import models
from django.templatetags.static import static


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name

    def get_friendly_name(self) -> str:
        return self.friendly_name or self.name


class Product(models.Model):
    """
    Image strategy:
    - Preferred: store a filename that lives in /static/images/  (e.g. 'pistachio-cake.jpg')
      Use Product.static_image_url in templates to render it.
    - Optional legacy: if you still have Cloudinary/remote URLs in the DB, put them in image_url.
      Your template can prefer image_filename, then fall back to image_url, then noimage.png.
    """
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )

    # NEW: filename relative to /static/images/
    image_filename = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Filename under static/images/, e.g. 'pistachio-cake.jpg'.",
    )

    # Optional legacy fallback (e.g. Cloudinary delivery URL or any remote URL)
    image_url = models.URLField(
        max_length=500, null=True, blank=True, help_text="Optional remote image URL."
    )

    def __str__(self) -> str:
        return self.name

    # -------- Convenience helpers for templates --------
    @property
    def static_image_url(self) -> str:
        """
        Returns a relative STATIC url for the image filename,
        or the project's 'noimage.png' if empty.
        """
        if self.image_filename:
            return static(f"images/{self.image_filename}")
        return static("images/noimage.png")
    @property
    def has_remote_image(self) -> bool:
        """True if a remote/Cloudinary URL is stored."""
        return bool(self.image_url)
