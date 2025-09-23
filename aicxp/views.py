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

        # --- 1. Semantic search (ürünler için) ---
        docs = semantic_search(q, k=5)
        ctx = "\n\n".join([f"{d['title']}: {d['content']}" for d in docs])

        # --- 2. Metrics ---
        metrics = None
        q_low = q.lower()
        if any(word in q_low for word in ["sepete", "satın", "roas", "ciro", "gelir", "tıklama"]):
            metrics = run_sql_metrics("adds", "2025-09-01", "2025-09-23", limit=7)

        # --- 3. Groq Prompt ---
        prompt = f"""
Sen CXP panelinin analitik ve ürün asistanısın.
Kullanıcı sorusunu veritabanından gelen bilgilerle cevapla.

Soru: {q}

Ürünler (semantic search sonucu):
{ctx or "Ürün bulunamadı."}

Metrikler:
{metrics or "Uygulanmadı"}

Cevabını kısa, net ve Türkçe ver.
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
