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
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.core.serializers import serialize


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
    today = timezone.now().date()
    default_start = today - timedelta(days=30)

    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else default_start
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else today
    except ValueError:
        return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    queryset = (
        UserEvent.objects.filter(
            event_name="add_to_cart",
            timestamp__date__gte=start_date,
            timestamp__date__lte=end_date,
        )
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    data = [{"day": str(entry["day"]), "count": entry["count"]} for entry in queryset]
    return JsonResponse(data, safe=False)



@require_GET
def user_events_list(request):
    """
    Kullanıcı eventlerini frontend için JSON olarak döner.
    """
    events = UserEvent.objects.all().order_by("-timestamp")[:500]  # Son 500 hareket (istersen arttır)
    data = []

    for event in events:
        data.append({
            "id": event.id,
            "event_name": event.event_name,
            "product_id": event.product_id,
            "user_id": event.user_id,
            "event_value": event.event_value,
            "timestamp": event.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return JsonResponse(data, safe=False)


def dashboard_stats(request):
    now = timezone.now()

    # Zaman aralıkları
    one_week_ago = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)

    # Toplam user event sayısı (son 7 gün)
    total_events_last_week = UserEvent.objects.filter(timestamp__gte=one_week_ago).count()

    # Önceki hafta
    total_events_prev_week = UserEvent.objects.filter(timestamp__gte=two_weeks_ago, timestamp__lt=one_week_ago).count()

    # Sepete ekleme sayısı (son 7 gün)
    add_to_cart_last_week = UserEvent.objects.filter(event_name="add_to_cart", timestamp__gte=one_week_ago).count()

    # Önceki hafta
    add_to_cart_prev_week = UserEvent.objects.filter(event_name="add_to_cart", timestamp__gte=two_weeks_ago, timestamp__lt=one_week_ago).count()

    # Yüzde değişim hesaplama
    def calculate_change(current, previous):
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return ((current - previous) / previous) * 100

    total_events_change = calculate_change(total_events_last_week, total_events_prev_week)
    add_to_cart_change = calculate_change(add_to_cart_last_week, add_to_cart_prev_week)

    data = {
        "total_events": {
            "count": total_events_last_week,
            "change": round(total_events_change, 2)
        },
        "add_to_cart": {
            "count": add_to_cart_last_week,
            "change": round(add_to_cart_change, 2)
        }
    }

    return JsonResponse(data)




@require_GET
def most_viewed_products(request):
    # URL parametrelerinden tarih aralığını al
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")

    try:
        # Parametre varsa kullan, yoksa son 30 günü al
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else timezone.now().date() - timedelta(days=30)
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else timezone.now().date()
    except ValueError:
        return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    # "view_item" event'ine göre en çok görüntülenen ürünleri bul
    queryset = (
        UserEvent.objects
        .filter(event_name="view_item", timestamp__date__gte=start_date, timestamp__date__lte=end_date)
        .values("product_id")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]  # ilk 10 ürün
    )

    # Sonuçları JSON formatına çevir
    data = [{"product_id": entry["product_id"], "count": entry["count"]} for entry in queryset]
    return JsonResponse(data, safe=False)