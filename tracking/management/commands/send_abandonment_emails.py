from django.core.management.base import BaseCommand
from django.utils import timezone
from tracking.models import CartAbandonment
from subscriptions.models import Subscriber
from subscriptions.utils import send_cart_abandonment_email

class Command(BaseCommand):
    help = "Send cart abandonment emails"

    def handle(self, *args, **kwargs):
        one_hour_ago = timezone.now() - timezone.timedelta(hours=1)
        abandons = CartAbandonment.objects.filter(
            added_at__lte=one_hour_ago,
            is_purchased=False,
            is_email_sent=False
        )

        for abandon in abandons:
            user_id = abandon.user_id
            product_id = abandon.product_id

            if "@" in user_id:  # user_id bir email ise
                email_sent = send_cart_abandonment_email(user_id, product_id)
                if email_sent:
                    abandon.is_email_sent = True
                    abandon.save()
                    self.stdout.write(self.style.SUCCESS(f"✔️ Mail gönderildi: {user_id}"))
                else:
                    self.stdout.write(self.style.ERROR(f"❌ Mail gönderilemedi: {user_id}"))
            else:
                self.stdout.write(f"⏭️ Geçersiz user_id: {user_id}")
