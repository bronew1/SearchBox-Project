from django.db import models
from django.http import JsonResponse
from django.utils import timezone

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

    # 🔥 Kaynak (ads, organic vs.)
    source = models.CharField(max_length=100, null=True, blank=True)

    # UTM alanları
    utm_source = models.CharField(max_length=255, null=True, blank=True)
    utm_medium = models.CharField(max_length=255, null=True, blank=True)
    utm_campaign = models.CharField(max_length=255, null=True, blank=True)
    utm_term = models.CharField(max_length=255, null=True, blank=True)
    utm_content = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.event_name} - {self.product_id} - {self.user_id}"


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


