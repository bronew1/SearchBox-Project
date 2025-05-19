from django.http import JsonResponse

from products.models import Product
from .services.ga4_api import fetch_search_terms
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from recommendations.models import UserInteraction
from products.models import Product
    

def search_terms_view(request):
    property_id = request.GET.get("property_id")
    if not property_id:
        return JsonResponse({"status": "error", "message": "GA4 mülk ID gerekli"}, status=400)

    try:
        terms = fetch_search_terms(property_id)
        return JsonResponse({"status": "success", "data": terms})
    except Exception as e:
        print("GA4 API Hatası:", e)  # 🔍 Buradan göreceğiz
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@csrf_exempt
def track_event(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            event_type = data.get("event_type")
            product_id = data.get("product_id")
            user_id = data.get("user_id")
            timestamp_str = data.get("timestamp")
            timestamp = parse_datetime(timestamp_str)

            product = Product.objects.filter(external_id=product_id).first()
            if not product:
                return JsonResponse({"status": "error", "message": "Product not found"}, status=404)

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
    return JsonResponse({"status": "invalid method"}, status=405)

#test macbook github
