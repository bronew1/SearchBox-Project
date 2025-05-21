from django.http import HttpResponse, JsonResponse
from .services.ga4_fetcher import get_top_products
from tracking.models import UserEvent
from products.models import Product  # senin ürün modelin buysa
from django.views.decorators.csrf import csrf_exempt

def trending_products(request):
    event_type = request.GET.get("type", "purchase")  # "purchase" veya "view_item"
    limit = int(request.GET.get("limit", 10))

    try:
        products = get_top_products(event_type=event_type, limit=limit)
        return JsonResponse({"products": products})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def get_recommendations(request):
    user_id = request.GET.get("user_id")

    if not user_id:
        return JsonResponse({"error": "user_id missing"}, status=400)

    # Bu kullanıcı geçmişte neleri görüntülemiş?
    events = UserEvent.objects.filter(user_id=user_id, event_name="view_item").order_by("-timestamp")

    # En son baktığı ürünlerden en fazla 10 tanesini çek
    product_ids = list(events.values_list("product_id", flat=True).distinct()[:10])

    # Ürünleri ürün tablosundan getir
    recommended_products = Product.objects.filter(external_id__in=product_ids)

    result = []
    for product in recommended_products:
        result.append({
            "name": product.name,
            "price": product.price,
            "image": product.image_url,
            "sku": product.external_id, 
        })

    return JsonResponse({"recommendationsz": result})