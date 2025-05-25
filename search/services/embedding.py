from sentence_transformers import SentenceTransformer
import numpy as np

# Model sadece bir kez yüklenmeli
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> list:
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
