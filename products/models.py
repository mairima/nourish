from django.db import models
from django.templatetags.static import static
from cloudinary.models import CloudinaryField


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        # Return category name
        return self.name

    def get_friendly_name(self):
        # Return friendly name or fallback to name
        return self.friendly_name or self.name


class Product(models.Model):
    category = models.ForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    image_filename = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    image = CloudinaryField("image", null=True, blank=True)

    def __str__(self):
        # Return product name
        return self.name

    @property
    def image_url_fixed(self):
        """
        Resolves:
        - CloudinaryField real image
        - Old Cloudinary URLs (fix .png → .jpg if needed)
        - Local filename
        - Fallback
        """

        # 1. CloudinaryField REAL upload
        try:
            if (
                self.image
                and hasattr(self.image, "url")
                and self.image.url
                and "placeholder" not in self.image.url
                and not self.image.url.endswith("/image/upload/placeholder")
            ):
                return self.image.url
        except Exception:
            pass

        # 2. Old Cloudinary URL
        if self.image_url:
            # Try .jpg version if .png fails
            url = self.image_url
            if url.endswith(".png"):
                return url[:-4] + ".jpg"
            return url

        # 3. Static filename
        if self.image_filename:
            return static(f"images/{self.image_filename}")

        # 4. fallback
        return static("images/noimage.png")


