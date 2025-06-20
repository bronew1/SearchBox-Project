from django.template import Template, Context
from django.core.mail import EmailMultiAlternatives
from subscriptions.models import EmailTemplateRecommendation

def send_recommendation_email(to_email, recommended_products):
    try:
        template = EmailTemplateRecommendation.objects.get(name="recommendation_v1")
    except EmailTemplateRecommendation.DoesNotExist:
        return False

    product_html = ""
    for p in recommended_products:
        product_html += f"""
            <div style="margin-bottom:20px; text-align:center;">
                <img src="{p['image']}" width="200" style="border-radius:8px;"><br>
                <strong>{p['name']}</strong><br>
                <span>{p['price']} TL</span><br>
                <a href="{p['url']}">Ürüne Git</a>
            </div>
        """

    template_str = template.html_content.replace("{{ recommended_products }}", product_html)
    subject = template.subject

    msg = EmailMultiAlternatives(subject=subject, body=template_str, to=[to_email])
    msg.attach_alternative(template_str, "text/html")
    msg.send()

    return True
