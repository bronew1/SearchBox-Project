from django.http import JsonResponse
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
