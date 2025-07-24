import os
import json
import logging
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import EmailTemplateWelcome, Subscriber
from .utils import send_welcome_email
from django.views.decorators.http import require_GET
from django.utils.dateparse import parse_date

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



@require_GET
def get_welcome_email_template(request):
    try:
        template = EmailTemplateWelcome.objects.get(name="welcome_email")
        data = {
            "name": template.name,
            "subject": template.subject,
            "html_content": template.html_content,
            "image_url": template.image.url if template.image else None,
        }
        return JsonResponse(data)
    except EmailTemplateWelcome.DoesNotExist:
        return JsonResponse({"error": "Template bulunamadı"}, status=404)
    

@csrf_exempt
@require_http_methods(["PATCH"])
def update_welcome_email_template(request):
    try:
        data = json.loads(request.body)

        template = EmailTemplateWelcome.objects.get(name="welcome_email")

        template.name = data.get("name", template.name)
        template.subject = data.get("subject", template.subject)
        template.html_content = data.get("html_content", template.html_content)
        template.save()

        return JsonResponse({"status": "ok"})
    except EmailTemplateWelcome.DoesNotExist:
        return JsonResponse({"error": "Template bulunamadı"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    

def subscribe_list(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    queryset = Subscriber.objects.all()

    if start_date:
        queryset = queryset.filter(subscribed_at__date__gte=parse_date(start_date))
    if end_date:
        queryset = queryset.filter(subscribed_at__date__lte=parse_date(end_date))

    data = [
        {
            "email": sub.email,
            "subscribed_at": sub.subscribed_at.isoformat()
        }
        for sub in queryset
    ]
    return JsonResponse(data, safe=False)
