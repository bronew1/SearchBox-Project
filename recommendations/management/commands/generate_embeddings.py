# recommendations/management/commands/generate_embeddings.py
import pickle
import os
from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer
from products.models import Product

class Command(BaseCommand):
    help = "Generate product embeddings using product name + description"

    def handle(self, *args, **kwargs):
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = {}

        for product in Product.objects.all():
            text = f"{product.name} {product.description or ''}"
            vector = model.encode(text)
            embeddings[product.sku] = vector

        output_path = "recommendations/embeddings.pkl"
        with open(output_path, "wb") as f:
            pickle.dump(embeddings, f)

        self.stdout.write(self.style.SUCCESS(f"Embeddings saved to {output_path}"))
