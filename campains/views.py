from pyexpat.errors import messages
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from products.models import Product
from tracking.models import UserEvent
from .models import EmailCampaign
import json
from django.views.decorators.http import require_http_methods


@csrf_exempt
def create_campaign(request):
    if request.method == "POST":
        data = json.loads(request.body)

        price_limit = data.get("price_limit")
        price_condition = data.get("price_condition")
        is_template = data.get("is_template", False)
        design_json = data.get("design_json")  # ✅ YENİ

        campaign = EmailCampaign.objects.create(
            title=data["title"],
            subject=data.get("subject", ""),
            html_content=data["html_content"],
            design_json=design_json,  # ✅ EKLENDİ
            segment=data.get("segment", ""),
            send_after_days=int(data.get("send_after_days", 0)),
            active=True,
            price_limit=float(price_limit) if price_limit else None,
            price_condition=price_condition if price_condition else None,
            is_template=is_template,
        )
        return JsonResponse({"status": "success", "id": campaign.id})
    return JsonResponse({"error": "Only POST allowed"}, status=405)





def list_campaigns(request):
    is_template = request.GET.get("is_template")

    campaigns = EmailCampaign.objects.all().order_by('-created_at')

    if is_template == "true":
        campaigns = campaigns.filter(is_template=True)
    else:
        # 🔥 Eğer parametre gelmezse bile varsayılan olarak kampanyaları dön
        campaigns = campaigns.filter(is_template=False)

    data = []
    for campaign in campaigns:
        data.append({
            "id": campaign.id,
            "title": campaign.title,
            "subject": campaign.subject,
            "segment": campaign.segment,
            "send_after_days": campaign.send_after_days,
            "created_at": campaign.created_at.strftime("%Y-%m-%d %H:%M"),
        })
    return JsonResponse(data, safe=False)




def campaign_detail(request, pk):
    try:
        campaign = EmailCampaign.objects.get(pk=pk)
    except EmailCampaign.DoesNotExist:
        raise Http404("Kampanya bulunamadı.")

    data = {
        "id": campaign.id,
        "title": campaign.title,
        "subject": campaign.subject,
        "segment": campaign.segment,
        "send_after_days": campaign.send_after_days,
        "html_content": campaign.html_content,
        "created_at": campaign.created_at.strftime("%Y-%m-%d %H:%M"),
    }
    return JsonResponse(data)



@csrf_exempt
@require_http_methods(["DELETE"])
def delete_campaign(request, pk):
    try:
        campaign = EmailCampaign.objects.get(pk=pk)
        campaign.delete()
        return JsonResponse({"status": "success", "message": "Kampanya başarıyla silindi."})
    except EmailCampaign.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Kampanya bulunamadı."}, status=404)


def get_target_users(campaign):
    if campaign.segment == "cart":
        events = UserEvent.objects.filter(event_name="add_to_cart")
    elif campaign.segment == "viewers":
        events = UserEvent.objects.filter(event_name="view_item")
    elif campaign.segment == "members":
        events = UserEvent.objects.filter(event_name="purchase")
    else:
        events = UserEvent.objects.none()

    # 💡 Eğer fiyat filtresi varsa
    if campaign.price_limit and campaign.price_condition:
        product_ids = events.values_list("product_id", flat=True)
        products = Product.objects.filter(external_id__in=product_ids)

        if campaign.price_condition == "higher":
            filtered_products = products.filter(price__gte=campaign.price_limit)
        else:
            filtered_products = products.filter(price__lte=campaign.price_limit)

        filtered_product_ids = filtered_products.values_list("external_id", flat=True)
        events = events.filter(product_id__in=filtered_product_ids)

    user_ids = events.values_list("user_id", flat=True).distinct()
    return user_ids

# Sonrasında diğer view fonksiyonların (create_campaign, list_campaigns vb.) devam eder
