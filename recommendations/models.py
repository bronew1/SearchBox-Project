# recommendations/models.py

from django.db import models

class CartAbandonment(models.Model):
    user_id = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email or self.user_id} - {self.product_id}"
