from django.db import models
from django.http import JsonResponse
from django.utils import timezone
import json
from .models import PushSubscription
from django.views.decorators.csrf import csrf_exempt

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


class CartAbandonment(models.Model):
    user_id = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    added_at = models.DateTimeField(default=timezone.now)
    is_purchased = models.BooleanField(default=False)
    is_email_sent = models.BooleanField(default=False)



class PushSubscription(models.Model):
    user_id = models.CharField(max_length=255)
    subscription_info = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


# tracking/models.py

class PushSubscription(models.Model):
    endpoint = models.TextField()
    keys_auth = models.CharField(max_length=256)
    keys_p256dh = models.CharField(max_length=256)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


@csrf_exempt
def save_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        endpoint = data.get("endpoint")
        keys = data.get("keys", {})
        auth = keys.get("auth")
        p256dh = keys.get("p256dh")
        user_id = request.COOKIES.get("user_id")  # veya başka bir user tracking metodu

        # kaydet veya güncelle
        PushSubscription.objects.update_or_create(
            endpoint=endpoint,
            defaults={
                "keys_auth": auth,
                "keys_p256dh": p256dh,
                "user_id": user_id
            }
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "invalid method"}, status=405)