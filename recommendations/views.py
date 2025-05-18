from django.http import HttpResponse, JsonResponse
from .services.ga4_fetcher import get_top_products

def trending_products(request):
    event_type = request.GET.get("type", "purchase")  # "purchase" veya "view_item"
    limit = int(request.GET.get("limit", 10))

    try:
        products = get_top_products(event_type=event_type, limit=limit)
        return JsonResponse({"products": products})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

