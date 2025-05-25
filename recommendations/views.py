from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from recommendations.services.ga4_fetcher import get_top_products
from tracking.models import UserEvent
from products.models import Product

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

    # Kullanıcının geçmişte görüntülediği ürünlerin kodlarını al (external_id veya sku olabilir)
    events = UserEvent.objects.filter(user_id=user_id, event_name="view_item").order_by("-timestamp")
    product_codes = list(events.values_list("product_id", flat=True).distinct()[:10])

    # SKU ya da external_id eşleşmelerini bul
    recommended_products = Product.objects.filter(sku__in=product_codes) | Product.objects.filter(external_id__in=product_codes)

    result = []
    for product in recommended_products:
        result.append({
            "name": product.name,
            "price": float(product.price),
            "image": product.image_url,
            "sku": product.sku or product.external_id,
        })

    return JsonResponse({"recommendationsz": result})



