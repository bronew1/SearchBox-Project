from django.core.management.base import BaseCommand
from django.db import connection
from products.models import Product  # kendi Product modeline göre kontrol et
from aicxp.utils import get_embedding

class Command(BaseCommand):
    help = "Ürünleri ai_documents tablosuna sync eder (embedding ile)"

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        count = 0

        with connection.cursor() as cursor:
            for p in products:
                content = f"{p.name}\n\n{p.description or ''}"
                emb = get_embedding(content).tolist()

                cursor.execute("""
                    INSERT INTO ai_documents (source_type, source_id, title, content, embedding, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s::vector, NOW(), NOW())
                    ON CONFLICT (source_id) DO UPDATE
                      SET title = EXCLUDED.title,
                          content = EXCLUDED.content,
                          embedding = EXCLUDED.embedding,
                          updated_at = NOW();
                """, ["product", str(p.id), p.name, content, emb])

                count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} ürün sync edildi"))
