from django.http import JsonResponse
from django.db.models import Q
from products.models import Product

def search_products(request):
    query = request.GET.get("q", "")
    if not query:
        return JsonResponse({"results": []})

    results = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )[:20]  # limit to 20 results

    data = [
        {
            "name": product.name,
            "sku": product.sku,
            "price": float(product.price),
            "image": product.image_url,
        }
        for product in results
    ]
    return JsonResponse({"results": data})
