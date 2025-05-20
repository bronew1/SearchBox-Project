from django.db import models
from products.models import Product  # Ürünün kaynağı

class UserInteraction(models.Model):
    user_id = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    event_type = models.CharField(max_length=50)  # örn: 'add_to_cart', 'purchase', 'view'
    timestamp = models.DateTimeField()
