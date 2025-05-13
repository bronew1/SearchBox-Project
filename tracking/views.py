# tracking/views.py
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import now

@csrf_exempt
def track_event(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            event_type = data.get("event_type")
            product_id = data.get("product_id")
            user_id = data.get("user_id")
            timestamp = data.get("timestamp")

            # Burada loglama veya kaydetme yapılabilir
            print("📦 Etkinlik alındı:", event_type, product_id, user_id, timestamp)

            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "invalid method"}, status=405)