from django.http import JsonResponse

from recommendations.services.ga4_fetcher import get_total_revenue
from .services.ga4_api import fetch_search_terms


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




def revenue_view(request):
    start_date = request.GET.get("start_date", "28daysAgo")
    end_date = request.GET.get("end_date", "today")
    try:
        revenue = get_total_revenue(start_date=start_date, end_date=end_date)
        return JsonResponse({"status": "success", "revenue": revenue})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)