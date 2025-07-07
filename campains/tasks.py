# apps/campains/tasks.py

from .brevo_utils import send_brevo_email
from tracking.models import UserEvent
from campains.models import EmailCampaign

import re

def is_valid_email(email):
    """Basit email doğrulama"""
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def process_email_campaigns():
    campaigns = EmailCampaign.objects.all()

    for campaign in campaigns:
        # Segment kontrolü eklemek istersen buraya koyabilirsin
        users = UserEvent.objects.all().distinct("user_id")

        for user in users:
            user_email = user.user_id.strip()

            if not is_valid_email(user_email):
                print(f"❌ Geçersiz, atlanıyor: {user_email}")
                continue

            # Brevo email gönder
            try:
                send_brevo_email(
                    subject=campaign.subject,
                    html_content=campaign.html_content,
                    to_email=user_email,
                )
                print(f"✅ Email gönderildi: {user_email}")
            except Exception as e:
                print(f"❌ Gönderim hatası: {e} - {user_email}")
