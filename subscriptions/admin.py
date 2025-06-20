from django.contrib import admin
from .models import EmailTemplateCartReminder, EmailTemplateRecommendation, EmailTemplateWelcome, Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):    list_display = ["email", "subscribed_at"]


@admin.register(EmailTemplateWelcome)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "subject")


@admin.register(EmailTemplateCartReminder)
class EmailTemplateCartReminderAdmin(admin.ModelAdmin):
    list_display = ("name", "subject")


admin.site.register(EmailTemplateRecommendation)