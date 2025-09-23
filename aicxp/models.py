from django.db import models

class AIDocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    source_type = models.TextField(null=True, blank=True)   # örn: "product", "event"
    source_id = models.TextField(unique=True)               # örn: ürün id
    title = models.TextField(null=True, blank=True)
    content = models.TextField()
    embedding = models.BinaryField(null=True, blank=True)   # vektörü burada binary saklayacağız
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_documents"

    def __str__(self):
        return self.title or f"Doc {self.id}"
