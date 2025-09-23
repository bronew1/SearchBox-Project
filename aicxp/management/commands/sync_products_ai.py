from django.core.management.base import BaseCommand
from django.db import connection
from sentence_transformers import SentenceTransformer
from products.models import Product  # ürün modelini kendi app adına göre düzelt

class Command(BaseCommand):
    help = "Product verilerini ai_documents tablosuna senkronize eder"

    def handle(self, *args, **options):
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        products = Product.objects.all()
        self.stdout.write(self.style.NOTICE(f"{products.count()} ürün işleniyor..."))

        with connection.cursor() as cursor:
            for p in products:
                content = f"{p.name} - {p.description or ''}"
                emb = model.encode([content], convert_to_numpy=True).tolist()[0]

                cursor.execute("""
                    INSERT INTO ai_documents (source_type, source_id, title, content, embedding, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                    ON CONFLICT (source_id)
                    DO UPDATE SET 
                        title = EXCLUDED.title,
                        content = EXCLUDED.content,
                        embedding = EXCLUDED.embedding,
                        updated_at = NOW();
                """, ["product", str(p.id), p.name, content, emb])

        self.stdout.write(self.style.SUCCESS("Ürünler başarıyla senkronize edildi."))
