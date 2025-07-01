from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from django.utils import timezone
from datetime import timedelta
from backend import settings
from tracking.models import CartAbandonment, PushSubscription, UserEvent
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.utils.timezone import now
from pywebpush import webpush
from django.http import FileResponse
import os
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.http import JsonResponse
from tracking.models import UserEvent


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




def send_push(subscription, message):
    webpush(
        subscription_info={
            "endpoint": subscription.endpoint,
            "keys": {
                "p256dh": subscription.keys_p256dh,
                "auth": subscription.keys_auth
            }
        },
        data=message,
        vapid_private_key=settings.VAPID_PRIVATE_KEY,
        vapid_claims={"sub": "mailto:berk.oztug@sinapirlanta.com"}
    )


def public_vapid_key(request):
    return HttpResponse(settings.VAPID_PUBLIC_KEY)


def service_worker(request):
    filepath = os.path.join(settings.BASE_DIR, 'static', 'service-worker.js')
    return FileResponse(open(filepath, 'rb'), content_type='application/javascript')

@csrf_exempt
def save_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        subscription = data.get("subscription", {})
        endpoint = subscription.get("endpoint")
        keys = subscription.get("keys", {})
        auth = keys.get("auth")
        p256dh = keys.get("p256dh")
        user_id = data.get("user_id") or request.COOKIES.get("user_id")

        if endpoint and auth and p256dh:
            PushSubscription.objects.update_or_create(
                endpoint=endpoint,
                defaults={
                    "keys_auth": auth,
                    "keys_p256dh": p256dh,
                    "user_id": user_id
                }
            )
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "missing data"}, status=400)

    return JsonResponse({"error": "invalid method"}, status=405)




def daily_add_to_cart_counts(request):
    # Son 30 gün
    from django.utils import timezone
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)

    queryset = (
        UserEvent.objects.filter(event_name="add_to_cart", timestamp__date__gte=last_30_days)
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    # JSON çıktısı: örn. [{"day": "2024-06-01", "count": 10}, ...]
    data = [{"day": str(entry["day"]), "count": entry["count"]} for entry in queryset]
    return JsonResponse(data, safe=False)
