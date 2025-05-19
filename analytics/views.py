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
        data = json.loads(request.body)
        print("📦 Etkinlik alındı:", data)
        return JsonResponse({"status": "ok"})

#test macbook github
