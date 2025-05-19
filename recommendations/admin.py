# recommendations/admin.py
from django.contrib import admin
from .models import UserInteraction

@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ("user_id", "product", "event_type", "timestamp")
    list_filter = ("event_type", "timestamp")
    search_fields = ("user_id", "product__title")
