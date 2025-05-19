from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from recommendations.models import UserInteraction
from products.models import Product
from django.http import JsonResponse



@csrf_exempt
def track_event(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # GA4-style parametreler
            event_type = data.get("event_type")            # Örn: view_item, add_to_cart, purchase
            product_id = data.get("product_id")            # Ürünün external_id'si
            user_id = data.get("user_id")                  # localStorage UUID'si
            timestamp_str = data.get("timestamp")          # ISO format datetime string
            timestamp = parse_datetime(timestamp_str)

            # Ürün veritabanında var mı kontrolü
            product = Product.objects.filter(external_id=product_id).first()
            if not product:
                return JsonResponse({"status": "error", "message": "Product not found"}, status=404)

            # Etkileşimi kaydet
            UserInteraction.objects.create(
                user_id=user_id,
                product=product,
                event_type=event_type,
                timestamp=timestamp
            )

            print("✅ Etkinlik kaydedildi:", event_type, product_id, user_id, timestamp_str)
            return JsonResponse({"status": "success"}, status=201)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    elif request.method == "GET":
        return JsonResponse({"status": "ok", "message": "Tracking endpoint is live (but expects POST)"})

    return JsonResponse({"status": "invalid method"}, status=405)
