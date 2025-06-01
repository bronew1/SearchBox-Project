# subscriptions/utils.py

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import EmailTemplate
import logging

logger = logging.getLogger('subscriptions')

def send_welcome_email(email):
    logger.info(f"📬 Mail fonksiyonu tetiklendi: {email}")

    try:
        template = EmailTemplate.objects.get(name="welcome_email")
    except EmailTemplate.DoesNotExist:
        logger.error("❌ 'welcome_email' isimli EmailTemplate bulunamadı.")
        return

    html_content = template.html_content
    text_content = "Merhaba, aramıza hoş geldiniz!"  # istersen admin'den de alınabilir
    subject = template.subject

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        "Sina Pırlanta <no-reply@sinapirlanta.email>",
        [email]
    )
    msg.attach_alternative(html_content, "text/html")

    if template.image:
        msg.attach_file(template.image.path)

    msg.send()
    logger.info("✅ Mail gönderildi")
