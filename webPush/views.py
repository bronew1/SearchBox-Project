import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PushSubscription
from pywebpush import webpush, WebPushException
from django.conf import settings


@csrf_exempt
def save_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)

        subscription = PushSubscription.objects.create(
            user_id=data.get("user_id"),
            endpoint=data["endpoint"],
            auth_key=data["keys"]["auth"],
            p256dh_key=data["keys"]["p256dh"],
        )

        return JsonResponse({"status": "success", "id": subscription.id})
    return JsonResponse({"error": "Only POST allowed"}, status=405)




def send_push_notification(subscription, message):
    try:
        webpush(
            subscription_info={
                "endpoint": subscription.endpoint,
                "keys": {
                    "p256dh": subscription.p256dh_key,
                    "auth": subscription.auth_key,
                }
            },
            data=message,
            vapid_private_key=settings.WEBPUSH_SETTINGS["VAPID_PRIVATE_KEY"],
            vapid_claims={
                "sub": settings.WEBPUSH_SETTINGS["VAPID_ADMIN_EMAIL"]
            }
        )
        return True
    except WebPushException as ex:
        print("Web push error:", repr(ex))
        return False
