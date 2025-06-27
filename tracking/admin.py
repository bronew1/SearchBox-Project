from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CartAbandonment, PushSubscription, UserEvent

@admin.register(UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    list_display = ["event_name", "product_id", "user_id", "timestamp"]
    list_filter = ["event_name", "timestamp"]

@admin.register(CartAbandonment)
class CartAbandonmentAdmin(admin.ModelAdmin):
    list_display = ["user_id", "product_id", "added_at", "is_purchased", "is_email_sent"]  # ✅ DOĞRU HALİ
    list_filter = ["is_email_sent", "is_purchased"]  # ✅ DOĞRU HALİ

@admin.register(PushSubscription)
class PushSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'user_id', 'created_at')
    search_fields = ('user_id', 'endpoint')