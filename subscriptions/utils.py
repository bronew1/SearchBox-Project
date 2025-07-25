from datetime import date, timedelta
from urllib import response
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import EmailTemplateCartReminder, EmailTemplateWelcome, Subscriber
import logging
from django.conf import settings
from subscriptions.models import EmailTemplateRecommendation
import requests
from recommendations.views import similar_products
from products.models import Product
from django.test import RequestFactory
import json
from django.template import Template, Context

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
    






def send_recommendation_email(to_email, sku):
    try:
        # 1. Şablonu al
        template = EmailTemplateRecommendation.objects.get(name="recommendation_v1")

        # 2. Benzer ürünleri al
        request = RequestFactory().get(f"/api/recommendations/similar/{sku}/")
        response = similar_products(request, sku=sku)
        data = json.loads(response.content)
        product_data = data.get("products", [])

        # 3. HTML oluştur
        recommended_html = """
        <table align="center" style="width:100%; max-width:600px; margin:auto;">
          <tr>
        """

        for p in product_data:
            product_sku = p.get("sku")
            try:
                product_obj = Product.objects.get(sku=product_sku)
                product_url = product_obj.product_url.strip() if product_obj.product_url else "#"
            except Product.DoesNotExist:
                print(f"⚠️ {product_sku} için ürün bulunamadı.")
                product_url = "#"

            if product_url == "#":
                print(f"⚠️ {product_sku} için product_url boş!")
            
            recommended_html += f"""
            <td style="text-align:center; padding:10px;">
              <img src="{p['image']}" alt="{p['name']}" width="120" style="border-radius:8px;"><br>
              <strong>{p['name']}</strong><br>
              <span>{int(p['price'])} TL</span><br>
              <a href="{product_url}" target="_blank" style="display:inline-block;margin-top:5px;padding:5px 10px;background:#ebbecb;color:#000;text-decoration:none;border-radius:4px;">İncele</a>
            </td>
            """

        recommended_html += "</tr></table>"

        # 4. Template içine göm
        template_engine = Template(template.html_content)
        context = Context({"recommended_products": recommended_html})
        html_content = template_engine.render(context)

        # 5. Mail gönder
        msg = EmailMultiAlternatives(
            template.subject,
            "",
            from_email="Sina Pırlanta <no-reply@sinapirlanta.email>",
            to=[to_email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        print("✅ Email başarıyla gönderildi.")
        return True

    except Exception as e:
        print("❌ Email gönderim hatası:", e)
        return False
    


def filter_subscribers(time_filter, start=None, end=None):
    today = date.today()
    if time_filter == "1d":
        return Subscriber.objects.filter(subscribed_at__gte=today - timedelta(days=1), is_active=True)
    elif time_filter == "3d":
        return Subscriber.objects.filter(subscribed_at__gte=today - timedelta(days=3), is_active=True)
    elif time_filter == "7d":
        return Subscriber.objects.filter(subscribed_at__gte=today - timedelta(days=7), is_active=True)
    elif time_filter == "30d":
        return Subscriber.objects.filter(subscribed_at__gte=today - timedelta(days=30), is_active=True)
    elif time_filter == "custom" and start and end:
        return Subscriber.objects.filter(subscribed_at__range=(start, end), is_active=True)
    return Subscriber.objects.filter(is_active=True)