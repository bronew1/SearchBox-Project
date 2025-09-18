import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from .utils import semantic_search, run_sql_metrics

client = OpenAI()

@csrf_exempt
def ask(request):
    """
    Kullanıcıdan gelen soruyu alır, önce semantic_search ile bağlam toplar,
    gerekirse run_sql_metrics ile metrik sorgular, sonra OpenAI modeline gönderir.
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    body = json.loads(request.body)
    question = body.get("question", "").strip()
    if not question:
        return JsonResponse({"error": "question boş olamaz"}, status=400)

    # Semantic search
    docs = semantic_search(question, k=5)
    context = "\n\n".join([f"{d['title']}:\n{d['content']}" for d in docs])

    # SQL metrics (basit örnek: eğer soru 'roas' kelimesi içeriyorsa)
    metrics = None
    if "roas" in question.lower():
        metrics = run_sql_metrics("roas", "2025-09-01", "2025-09-18")  # tarihleri dinamik verebilirsin

    prompt = f"""
    Sen CXP panelinin akıllı asistanısın.
    PostgreSQL verilerinden gelen metrikler ve semantic search bağlamını kullanarak soruları yanıtla.

    BAĞLAM:
    {context}

    METRİKLER:
    {metrics}

    SORU: {question}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response.choices[0].message.content
    return JsonResponse({"answer": answer})
