import numpy as np
from sentence_transformers import SentenceTransformer
from django.db import connection

# Modeli global yükle (Performans için)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_embedding(text: str) -> np.ndarray:
    """Metinden embedding üret."""
    return np.array(model.encode(text), dtype=np.float32)

def semantic_search(query: str, limit: int = 5):
    """Postgres'te semantic search yap."""
    query_embedding = get_embedding(query).tolist()
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, title, content
            FROM ai_documents
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
            """,
            [query_embedding, limit],
        )
        rows = cursor.fetchall()
    results = [{"id": r[0], "title": r[1], "content": r[2]} for r in rows]
    return results
