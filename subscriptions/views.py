from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Subscriber
from .utils import send_welcome_email
import json

@csrf_exempt
def subscribe(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST bekleniyor"}, status=405)
    try:
        data = json.loads(request.body)
        email = data.get("email")
        if not email:
            return JsonResponse({"error": "email eksik"}, status=400)

        subscriber, created = Subscriber.objects.get_or_create(email=email)
        if created:
            send_welcome_email(email)

        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
