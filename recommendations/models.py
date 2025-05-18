# recommendations/models.py

from django.db import models
from products.models import Product

class UserInteraction(models.Model):
    user_id = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=[
        ('view', 'Viewed'),
        ('cart', 'Added to Cart'),
        ('purchase', 'Purchased'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.product.title} ({self.interaction_type})"
