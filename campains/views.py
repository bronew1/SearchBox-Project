from pyexpat.errors import messages
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import EmailCampaign
import json
from django.views.decorators.http import require_http_methods


@csrf_exempt
def create_campaign(request):
    if request.method == "POST":
        data = json.loads(request.body)
        campaign = EmailCampaign.objects.create(
            title=data["title"],
            subject=data["subject"],
            html_content=data["html_content"],
            segment=data["segment"],
            send_after_days=int(data["send_after_days"]),
            active=True,
        )
        return JsonResponse({"status": "success", "id": campaign.id})
    return JsonResponse({"error": "Only POST allowed"}, status=405)

def list_campaigns(request):
    campaigns = EmailCampaign.objects.all().order_by('-created_at')
    data = []
    for campaign in campaigns:
        data.append({
            "id": campaign.id,
            "title": campaign.title,
            "subject": campaign.subject,
            "segment": campaign.segment,
            "send_after_days": campaign.send_after_days,  # ✅ düzeltildi
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
