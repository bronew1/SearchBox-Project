import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aicxp.utils import semantic_search, run_sql_metrics
from groq import Groq

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"  # hızlı + ücretsiz model

@csrf_exempt
def ask(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        body = json.loads(request.body)
        q = body.get("question", "").strip()

        if not q:
            return JsonResponse({"error": "question boş"}, status=400)

        q_low = q.lower()
        docs = []

        # --- 1. Eğer kullanıcı "hepsini listele" derse -> tümünü çek ---
        if "hepsini" in q_low or "tamamını" in q_low or "listele" in q_low:
            with connection.cursor() as cur:
                cur.execute("""
                    SELECT id, title, content
                    FROM ai_documents
                    WHERE source_type='product'
                    AND (title ILIKE %s OR content ILIKE %s)
                    LIMIT 100
                """, (f"%tektaş%", f"%tektaş%"))
                rows = cur.fetchall()
                docs = [{"id": r[0], "title": r[1], "content": r[2]} for r in rows]
        else:
            # --- 2. Normal semantic search ---
            docs = semantic_search(q, k=5)

        ctx = "\n\n".join([f"{d['title']}: {d['content']}" for d in docs])

        # --- 3. Metrics (örnek: sepete ekleme, satış vs.) ---
        metrics = None
        if any(word in q_low for word in ["sepete", "satın", "roas", "ciro", "gelir", "tıklama"]):
            metrics = run_sql_metrics("adds", "2025-09-01", "2025-09-23", limit=7)

        # --- 4. OpenAI/Groq prompt ---
        prompt = f"""
Sen Sina Pırlanta'nın CXP AI Asistanısın.
Kullanıcı sorusunu veritabanındaki ürünler ve metrikler ile cevapla.

Soru: {q}

Ürünler:
{ctx or "Ürün bulunamadı."}

Metrikler:
{metrics or "Yok"}

Cevabını kullanıcıya kısa, net ve Türkçe ver.
"""
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        return JsonResponse({
            "answer": resp.choices[0].message.content,
            "products": docs,
            "metrics": metrics
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
