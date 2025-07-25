from django.db import models


class Product(models.Model):
    external_id = models.CharField(max_length=100, unique=True)  # <g:id>
    sku = models.CharField(max_length=100, blank=True, null=True, db_index=True)  # <g:mpn>, öneri için önemli
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    category = models.CharField(max_length=100, blank=True)
    product_url = models.URLField(blank=True, null=True)  # Yeni alan
    
    def __str__(self):
        return f"{self.sku or self.external_id} - {self.name}"




class WidgetProduct(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField()
    hover_image_url = models.URLField(blank=True, null=True)
    price = models.CharField(max_length=50)
    product_url = models.URLField()
    sku = models.CharField(max_length=100, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order + 1}. {self.name}"