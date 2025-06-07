from django.core.management.base import BaseCommand
from django.utils import timezone
from tracking.models import CartAbandonment
from subscriptions.utils import send_cart_abandonment_email

class Command(BaseCommand):
    help = "Send cart abandonment emails"

    def handle(self, *args, **kwargs):
        limit_time = timezone.now() - timezone.timedelta(seconds=30)
        abandons = CartAbandonment.objects.filter(
            added_at__lte=limit_time,
            is_purchased=False,
            is_email_sent=False
        )

        for abandon in abandons:
            user_id = abandon.user_id
            product_id = abandon.product_id

            if "@" in user_id:  # ✅ sadece e-posta içeren kullanıcılar
                print(f"📧 Mail gönderimi deneniyor: {user_id}")
                email_sent = send_cart_abandonment_email(user_id, product_id)
                if email_sent:
                    abandon.is_email_sent = True
                    abandon.save()
                    self.stdout.write(self.style.SUCCESS(f"✔️ Mail gönderildi: {user_id}"))
                else:
                    self.stdout.write(self.style.ERROR(f"❌ Mail gönderilemedi: {user_id}"))
            else:
                self.stdout.write(f"⏭️ Geçersiz user_id: {user_id}")
