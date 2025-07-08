from django.db import models
from django.http import JsonResponse
from django.utils import timezone

class UserEvent(models.Model):
    EVENT_CHOICES = [
        ('view_item', 'View Item'),
        ('add_to_cart', 'Add to Cart'),
        ('purchase', 'Purchase'),
    ]

    SOURCE_CHOICES = [
        ('organic', 'Organik'),
        ('mail', 'Mail Kampanyası'),
        ('ads', 'Reklam'),
        ('affiliate', 'Affiliate'),
        ('other', 'Diğer'),
    ]

    event_name = models.CharField(max_length=50, choices=EVENT_CHOICES)
    product_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='organic')  # ✅ EKLENDİ
    event_value = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.event_name} - {self.product_id} - {self.user_id} - {self.source}"


class CartAbandonment(models.Model):
    user_id = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    added_at = models.DateTimeField(default=timezone.now)
    is_purchased = models.BooleanField(default=False)
    is_email_sent = models.BooleanField(default=False)



class PushSubscription(models.Model):
    endpoint = models.TextField()
    keys_auth = models.CharField(max_length=256)
    keys_p256dh = models.CharField(max_length=256)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


