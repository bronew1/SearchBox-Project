# recommendations/utils.py

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_similar_products(target_sku, product_embeddings, top_n=5):
    if target_sku not in product_embeddings:
        return []

    target_vector = product_embeddings[target_sku].reshape(1, -1)
    all_skus = list(product_embeddings.keys())
    all_vectors = np.array([product_embeddings[sku] for sku in all_skus])
    
    similarities = cosine_similarity(target_vector, all_vectors)[0]
    sku_similarities = list(zip(all_skus, similarities))
    sku_similarities.sort(key=lambda x: x[1], reverse=True)
    
    similar_skus = [sku for sku, _ in sku_similarities if sku != target_sku][:top_n]
    return similar_skus
