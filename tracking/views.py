import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserInteraction
from products.models import Product
from django.utils.dateparse import parse_datetime

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
                timestamp=timestamp,
            )
            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)
