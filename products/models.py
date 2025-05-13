from django.db import models

from django.db import models

class Product(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title
