from django.http import JsonResponse
from .services.ga4_api import fetch_search_terms
import json

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