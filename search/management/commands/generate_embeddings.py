from django.core.management.base import BaseCommand
from products.models import Product
from search.services.embedding import get_embedding
import json

class Command(BaseCommand):
    help = "Tüm ürünler için embedding hesaplar ve product.embedding alanına kaydeder."

    def handle(self, *args, **kwargs):
        success = 0
        fail = 0

        for product in Product.objects.all():
            try:
                text = f"{product.name} {product.description}"
                embedding = get_embedding(text)
                product.embedding = json.dumps(embedding)  # JSON olarak kaydet
                product.save()
                success += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Hata ({fail}): {e}"))
                fail += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Başarılı: {success}, ❌ Hatalı: {fail}"))
