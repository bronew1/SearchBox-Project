# your_tracking_app/models.py
from django.db import models

class CustomerEvent(models.Model):
    event_type = models.CharField(max_length=50) # 'add_to_cart', 'view_item', 'purchase'
    customer_id = models.CharField(max_length=255, blank=True, null=True) # Müşteri ID'si (varsa)
    session_id = models.CharField(max_length=255, blank=True, null=True) # Oturum ID'si (varsa)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    transaction_id = models.CharField(max_length=255, blank=True, null=True) # Satın alma için
    revenue = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # Satın alma için
    timestamp = models.DateTimeField(auto_now_add=True)
    raw_data = models.JSONField(blank=True, null=True) # Gelen tüm JSON verisini saklamak için

    def __str__(self):
        return f"{self.event_type} - {self.product_name or self.transaction_id} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"