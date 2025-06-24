from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.utils import timezone
from datetime import timedelta
from tracking.models import CartAbandonment, UserEvent
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.utils.timezone import now

@csrf_exempt
def track_event(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            event_name = data.get("event_name")
            product_id = data.get("product_id")
            event_value = data.get("event_value")
            user_id = data.get("user_id")

            # UserEvent olarak kaydet
            UserEvent.objects.create(
                event_name=event_name.strip(),
                product_id=product_id.strip() if product_id else None,
                event_value=event_value,
                user_id=user_id.strip()
            )

            # Sepete ekleme eventi
            if event_name == "add_to_cart" and product_id and user_id:
                CartAbandonment.objects.create(
                    user_id=user_id.strip(),
                    product_id=product_id.strip()
                )

            # Satın alma eventi
            if event_name == "purchase" and product_id and user_id:
                CartAbandonment.objects.filter(
                    user_id=user_id.strip(),
                    product_id=product_id.strip(),
                    is_purchased=False
                ).update(is_purchased=True)

            print(f"📦 Etkinlik: {event_name}, Ürün: {product_id}, Değer: {event_value}, Kullanıcı: {user_id}")
            return JsonResponse({"status": "ok"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)


def cart_count(request, product_id):
    last_day = timezone.now() - timedelta(days=1)

    count = UserEvent.objects.filter(
        event_name="add_to_cart",
        product_id=product_id,
        timestamp__gte=last_day
    ).values("user_id").distinct().count()

    return JsonResponse({"count": count})



def daily_add_to_cart_stats(request):
    days = 7
    end_date = now().date()
    start_date = end_date - timedelta(days=days)

    data = (
        UserEvent.objects
        .filter(event_name="add_to_cart", created_at__date__range=(start_date, end_date))
        .annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )

    return JsonResponse(list(data), safe=False)