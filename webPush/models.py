from django.db import models

class PushSubscription(models.Model):
    user_id = models.CharField(max_length=255)
    endpoint = models.TextField()
    auth_key = models.CharField(max_length=255)
    p256dh_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscription for {self.user_id}"
