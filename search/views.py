from django.http import JsonResponse
from django.db.models import Q
from products.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from search.models import ProductEmbedding
from search.services.embedding import get_embedding, cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
from search.models import ProductEmbedding

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

@csrf_exempt
def search_products(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"error": "Sorgu eksik"}, status=400)

    query_embedding = model.encode(query)

    results = []
    for pe in ProductEmbedding.objects.select_related("product").all():
        if pe.embedding:
            try:
                emb = np.array(pe.embedding)
                score = cosine_similarity(query_embedding, emb)
                results.append((score, pe.product))
            except Exception as e:
                print("Embedding karşılaştırma hatası:", e)

    # En yüksek benzerliğe sahip ilk 60 ürünü getir
    top_matches = sorted(results, key=lambda x: x[0], reverse=True)[:60]

    response = []
    for score, product in top_matches:
        response.append({
            "name": product.name,
            "sku": product.sku,
            "price": float(product.price),
            "image": product.image_url,
        })

    return JsonResponse({"results": response})

@require_GET
@csrf_exempt
def semantic_search(request):
    query = request.GET.get("q")
    if not query:
        return JsonResponse({"error": "Query param 'q' is required."}, status=400)

    query_embedding = get_embedding(query)

    results = []
    for pe in ProductEmbedding.objects.select_related("product").all():
        similarity = cosine_similarity(query_embedding, pe.embedding)
        results.append((similarity, pe.product))

    top_matches = sorted(results, key=lambda x: x[0], reverse=True)[:20]

    return JsonResponse({
        "results": [
            {
                "name": p.name,
                "sku": p.sku,
                "price": float(p.price),
                "image": p.image_url
            }
            for _, p in top_matches
        ]
    })