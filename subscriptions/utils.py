from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_welcome_email(email):
    logger.info(f"📬 Mail fonksiyonu tetiklendi: {email}")

    subject = "Aramıza Hoş Geldin!"
    from_email = settings.DEFAULT_FROM_EMAIL  # Buraya dikkat!
    to = [email]
    text_content = "Merhaba, aramıza hoş geldiniz!"
    html_content = render_to_string("email/welcome.html", {"email": email})

    logger.info("✅ HTML içerik oluşturuldu")

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    logger.info("✅ Mail gönderildi")
