from urllib import response
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import EmailTemplateCartReminder, EmailTemplateWelcome
import logging
from django.conf import settings
from subscriptions.models import EmailTemplateRecommendation
import requests
from recommendations.views import similar_products
from products.models import Product
from django.test import RequestFactory

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

def send_cart_abandonment_email(user_id, product_id):
    try:
        # user_id e-posta ise direkt kullan
        email = user_id if "@" in user_id else None
        if not email:
            return False

        subject = "Sepetinizde Ürün Kaldı!"
        text_content = "Sepetinizde ürün kaldı, alışverişinize devam etmek ister misiniz?"
        html_content = render_to_string("email/cart_reminder.html", {
            "product_id": product_id,
            "user_id": user_id,
        })

        msg = EmailMultiAlternatives(subject, text_content, "Sina Pırlanta <no-reply@sinapirlanta.email>", [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return True
    except Exception as e:
        logger.error(f"Sepet maili gönderilemedi: {str(e)}")
        return False


def send_cart_abandonment_email(user_id, product_id):
    try:
        email = user_id if "@" in user_id else None
        if not email:
            return False

        template = EmailTemplateCartReminder.objects.get(name="cart_reminder")
        subject = template.subject or "Sepetinizde Ürün Kaldı!"
        html_content = template.html_content or ""
        text_content = "Sepetinizde ürün kaldı, alışverişinize devam etmek ister misiniz?"

        if not html_content and template.image:
            html_content = f'<div style="text-align:center;"><img src="{template.image.url}" alt="Sepet Hatırlatma Görseli"></div>'

        msg = EmailMultiAlternatives(subject, text_content, "Sina Pırlanta <no-reply@sinapirlanta.email>", [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except Exception as e:
        logger.error(f"Sepet maili gönderilemedi: {str(e)}")
        return False
    



def send_recommendation_email(to_email, sku="SP21930"):
    try:
        # Admin panelinden template çek
        try:
            template = EmailTemplateRecommendation.objects.get(name="recommendation_v1")
        except EmailTemplateRecommendation.DoesNotExist:
            print("❌ Email gönderim hatası: EmailTemplateRecommendation bulunamadı (name='recommendation_v1')")
            return False

        # API view'ı çağır
        request = RequestFactory().get(f"/api/recommendations/similar/{sku}/")
        response = similar_products(request, sku=sku)

        # response.content içeriğini parse et
        data = json.loads(response.content)
        product_data = data.get("products", [])

        # HTML kartları oluştur
        recommended_html = ""
        for p in product_data:
            recommended_html += f"""
                <div style="display:inline-block; text-align:center; margin:10px;">
                    <img src="{p['image']}" alt="{p['name']}" width="140"><br>
                    <strong>{p['name']}</strong><br>
                    <span>{p['price']} TL</span><br>
                    <a href="{p['url']}" style="display:inline-block;margin-top:5px;padding:5px 10px;background:#ebbecb;color:#000;text-decoration:none;border-radius:4px;">İncele</a>
                </div>
            """

        # Şablon içine göm
        html_content = template.html_content.replace("{{ recommended_products }}", recommended_html)

        # Mail gönderimi
        msg = EmailMultiAlternatives(template.subject, "", to=[to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        print("✅ Email başarıyla gönderildi.")
        return True

    except Exception as e:
        print("❌ Email gönderim hatası:", e)
        return False