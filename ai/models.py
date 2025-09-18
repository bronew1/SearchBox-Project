from django.db import models
from django.utils.timezone import now

class AIDocument(models.Model):
    source_type = models.CharField(max_length=50)
    source_id = models.CharField(max_length=100, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    content = models.TextField()
    embedding = models.BinaryField(null=True, blank=True)  # pgvector için ayrı handle
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
