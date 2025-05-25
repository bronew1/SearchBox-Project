from django.db import models
from products.models import Product

class ProductEmbedding(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    embedding = models.JSONField()  # Embedding vektörü burada tutulacak

    def __str__(self):
        return f"Embedding for {self.product.sku}"
