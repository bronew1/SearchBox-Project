from django.db import models
from products.models import Product

class UserInteraction(models.Model):
    user_id = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    event_type = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return f"{self.user_id} - {self.event_type} - {self.product.title}"
