from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserEvent

@admin.register(UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    list_display = ["event_name", "product_id", "user_id", "timestamp"]
    list_filter = ["event_name", "timestamp"]
