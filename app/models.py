
from django.db import models


class Properties(models.Model):

    # Existing fields — preserved for compatibility
    furnished = models.CharField(max_length=100, blank=True, default='')
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    bhk = models.IntegerField(default=0)

    contact = models.CharField(max_length=15, blank=True, default='')

    house_image = models.ImageField(
        upload_to="properties/",
        blank=True,
        null=True
    )

    hall_image = models.ImageField(
        upload_to="properties/",
        blank=True,
        null=True
    )

    published = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    # New fields received from the admin panel
    source_property_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        unique=True
    )

    title = models.CharField(max_length=200, blank=True, default='')

    property_type = models.CharField(
        max_length=30,
        blank=True,
        default=''
    )

    purpose = models.CharField(
        max_length=20,
        blank=True,
        default=''
    )

    city = models.CharField(max_length=100, blank=True, default='')

    bathrooms = models.PositiveIntegerField(default=0)

    area = models.PositiveIntegerField(default=0)

    description = models.TextField(blank=True, default='')

    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title or self.furnished or f"Property {self.pk}"


class PropertyImage(models.Model):

    property = models.ForeignKey(
        Properties,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="properties/")

    image_type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.property} - {self.image_type}"
