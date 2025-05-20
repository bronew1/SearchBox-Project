from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from tracking.models import UserEvent

@csrf_exempt
def track_event(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            event_name = data.get("event_name")
            product_id = data.get("product_id")
            event_value = data.get("event_value")
            user_id = data.get("user_id")  # IP veya localStorage'dan da olabilir
            #db ye kaydetmek için
            UserEvent.objects.create(
                event_name=event_name,
                product_id=product_id,
                event_value=event_value,
                user_id=user_id
            )

            print(f"📦 Etkinlik: {event_name}, Ürün: {product_id}, Değer: {event_value}, Kullanıcı: {user_id}")

            return JsonResponse({"status": "ok"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)
