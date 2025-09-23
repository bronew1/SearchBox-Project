from django.core.management.base import BaseCommand
from products.models import Product
from ai.models import AIDocument
from ai.utils import get_embedding
from django.db import connection

class Command(BaseCommand):
    help = "Sync products into ai_documents table with embeddings"

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        count = 0

        with connection.cursor() as cursor:
            for product in products:
                content = f"{product.name} - {product.description or ''}"
                emb = get_embedding(content)

                cursor.execute(
                    """
                    INSERT INTO ai_documents (source_type, source_id, title, content, embedding, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s::vector, NOW(), NOW())
                    ON CONFLICT (source_id) DO UPDATE
                    SET title = EXCLUDED.title,
                        content = EXCLUDED.content,
                        embedding = EXCLUDED.embedding,
                        updated_at = NOW();
                    """,
                    ["product", str(product.id), product.name, content, emb.tolist()],
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} products synced into ai_documents"))
