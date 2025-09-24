from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, os
from groq import Groq
from aicxp.utils import semantic_search, run_sql_metrics, top_cart_product

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

from aicxp.utils import semantic_search, run_sql_metrics, top_products

@csrf_exempt
def ask(request):
    ...
    q_low = q.lower()
    metrics = None
    top = None

    # Eğer kullanıcı en çok sepete eklenen / görüntülenen ürünleri sorarsa
    if "sepete" in q_low and ("en çok" in q_low or "en fazla" in q_low):
        top = top_products("add_to_cart", limit=5)
    elif "görüntülenen" in q_low and ("en çok" in q_low or "en fazla" in q_low):
        top = top_products("view_item", limit=5)
    elif "satılan" in q_low or "satış" in q_low:
        top = top_products("purchase", limit=5)

    # Prompt içine ekle
    prompt = f"""
Sen Sina Pırlanta'nın akıllı müşteri asistanısın.
Görevin: Kullanıcıya doğal, samimi ve anlaşılır şekilde yanıt vermek.

Soru: {q}

İlgili ürünler:
{ctx or "Ürün bulunamadı."}

Top ürünler:
{top or "Yok"}

Metrikler:
{metrics or "Yok"}
"""

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    answer = resp.choices[0].message.content.strip() if resp.choices else ""

    if not answer:
        if top:
            answer = "İşte en popüler ürünlerimiz 😊:\n" + "\n".join([f"- {t['product_id']} ({t['count']} kez)" for t in top])
        elif docs:
            answer = "Bunları buldum:\n" + ctx
        else:
            answer = "Şu an elimde bu konuda bilgi yok 🙏"

    return JsonResponse({
        "answer": answer,
        "products": docs,
        "metrics": metrics,
        "top": top,
    })
