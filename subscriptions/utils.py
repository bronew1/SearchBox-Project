from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import logging
logger = logging.getLogger('subscriptions')

def send_welcome_email(email):
    logger.info(f"📬 Mail fonksiyonu tetiklendi: {email}")
    subject = "Aramıza Hoş Geldin!"
    from django.template.loader import render_to_string
    from django.core.mail import EmailMultiAlternatives

    html_content = render_to_string("email/welcome.html", {"email": email})
    text_content = "Merhaba, aramıza hoş geldiniz!"

    logger.info("✅ HTML içerik oluşturuldu")

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        "SearchProjectDemo <no-reply@searchprojectdemo.com>",
        [email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    logger.info("✅ Mail gönderildi")
