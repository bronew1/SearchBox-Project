from django.db import models

class UserEvent(models.Model):
    EVENT_CHOICES = [
        ('view_item', 'View Item'),
        ('add_to_cart', 'Add to Cart'),
        ('purchase', 'Purchase'),
    ]
    
    event_name = models.CharField(max_length=50, choices=EVENT_CHOICES)
    product_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    event_value = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.event_name} - {self.product_id} - {self.user_id}"
