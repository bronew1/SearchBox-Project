from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import EmailCampaign
from tracking.models import UserEvent  # Event modelini senin kullanıma göre düzenle
from .brevo_utils import send_brevo_email

@shared_task
def process_email_campaigns():
    campaigns = EmailCampaign.objects.filter(active=True)
    for campaign in campaigns:
        if campaign.segment == "cart":
            users = UserEvent.objects.filter(event_name="add_to_cart")
        elif campaign.segment == "viewers":
            users = UserEvent.objects.filter(event_name="view_item")
        elif campaign.segment == "members":
            users = UserEvent.objects.filter(event_name="login")
        else:
            users = []

        for user_event in users:
            if user_event.timestamp <= timezone.now() - timedelta(days=campaign.send_after_days):
                send_brevo_email(campaign.subject, campaign.html_content, user_event.user_id)
