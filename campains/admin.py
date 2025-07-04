from django.contrib import admin
from .models import EmailCampaign

@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ["title", "segment", "send_after_days", "active"]
