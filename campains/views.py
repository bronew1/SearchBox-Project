from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import EmailCampaign
import json

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