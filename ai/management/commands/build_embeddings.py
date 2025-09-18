from django.core.management.base import BaseCommand
from django.db import connection
from sentence_transformers import SentenceTransformer

class Command(BaseCommand):
    help = "Yerel sentence-transformers ile ai_documents için embedding üretir"

    def handle(self, *args, **opts):
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        with connection.cursor() as cur:
            cur.execute("""
                select id, content from ai_documents
                where embedding is null
                limit 500
            """)
            rows = cur.fetchall()

        if not rows:
            self.stdout.write(self.style.SUCCESS("Yeni içerik yok."))
            return

        texts = [r[1] for r in rows]
        vectors = model.encode(texts, convert_to_numpy=True)

        with connection.cursor() as cur:
            for (doc_id, _), vec in zip(rows, vectors):
                # Listeyi PostgreSQL pgvector formatına çevir: {0.12,-0.43,...}
                vec_str = "[" + ",".join(str(x) for x in vec.tolist()) + "]"
                cur.execute(
                    "update ai_documents set embedding = %s::vector where id = %s",
                    (vec_str, doc_id)
                )

        self.stdout.write(self.style.SUCCESS(f"{len(rows)} embedding güncellendi."))
