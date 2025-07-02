import os
import json
import logging

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Subscriber
from .utils import send_welcome_email

logger = logging.getLogger('subscriptions')

@csrf_exempt
def subscribe(request):
    # Fiziksel dosyaya log yaz
    log_path = os.path.join(os.path.dirname(__file__), "test.txt")
    with open(log_path, "a") as f:
        f.write("✅ subscribe fonksiyonuna girildi\n")

    if request.method == "GET":
        with open(log_path, "a") as f:
            f.write("👀 GET method çalıştı, liste dönülüyor\n")
        subscribers = Subscriber.objects.all().order_by("-subscribed_at")
        data = [
            {
                "email": sub.email,
                "subscribed_at": sub.subscribed_at
            }
            for sub in subscribers
        ]
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            with open(log_path, "a") as f:
                f.write(f"📥 Alınan email: {email}\n")

            if not email:
                return JsonResponse({"error": "email eksik"}, status=400)

            subscriber, created = Subscriber.objects.get_or_create(email=email)

            logger.info(f"📥 Popup'tan alınan email: {email}")
            logger.info(f"🆕 Oluşturuldu mu?: {created}")

            with open(log_path, "a") as f:
                f.write(f"🆕 Oluşturuldu mu?: {created}\n")

            if created:
                logger.info("📨 send_welcome_email çağrıldı")
                with open(log_path, "a") as f:
                    f.write("📨 send_welcome_email çağrıldı\n")
                send_welcome_email(email)

            return JsonResponse({"status": "ok"})

        except Exception as e:
            logger.error(f"❌ Hata oluştu: {str(e)}")
            with open(log_path, "a") as f:
                f.write(f"❌ Hata oluştu: {str(e)}\n")
            return JsonResponse({"error": str(e)}, status=400)

    # POST ve GET dışındaki methodlar
    with open(log_path, "a") as f:
        f.write("❌ Desteklenmeyen method, hata döndürüldü\n")
    return JsonResponse({"error": "Sadece GET veya POST desteklenir."}, status=405)
