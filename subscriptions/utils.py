from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import EmailTemplateWelcome
import logging

logger = logging.getLogger('subscriptions')

def send_welcome_email(email):
    logger.info(f"📬 Mail fonksiyonu tetiklendi: {email}")
    subject = "Hoş Geldiniz"

    try:
        template = EmailTemplateWelcome.objects.get(name="welcome_email")
    except EmailTemplateWelcome.DoesNotExist:
        logger.error("❌ 'welcome_email' isimli EmailTemplate bulunamadı.")
        return

    html_content = template.html_content.strip() if template.html_content else ""
    
    # Eğer html_content boşsa ama görsel varsa, görseli ekle
    if not html_content and template.image:
        html_content = f'<div style="text-align:center;"><img src="{template.image.url}" alt="Hoş Geldin Görseli"></div>'
    
    # Eğer tamamen boşsa, bir varsayılan mesaj koy
    if not html_content:
        html_content = f"<p>Hoş geldiniz {email}, aramıza katıldığınız için teşekkürler.</p>"

    text_content = "Merhaba, aramıza hoş geldiniz!"

    msg = EmailMultiAlternatives(
        template.subject or subject,
        text_content,
        "Sina Pırlanta <no-reply@sinapirlanta.email>",
        [email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    logger.info("✅ Mail gönderildi")
