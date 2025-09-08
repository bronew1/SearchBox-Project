from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class GeneratedAsset(models.Model):
    STATUS = [
        ("queued", "queued"),
        ("processing", "processing"),
        ("completed", "completed"),
        ("failed", "failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    prompt = models.TextField()
    negative_prompt = models.TextField(blank=True, default="")
    goal = models.CharField(max_length=50, blank=True)
    ad_type = models.CharField(max_length=50, blank=True)
    cta = models.CharField(max_length=120, blank=True)
    slogan = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    size = models.CharField(max_length=10, default="1:1")
    seed = models.BigIntegerField(null=True, blank=True)
    style_preset = models.CharField(max_length=50, blank=True)
    product_image = models.ImageField(upload_to="uploads/", null=True, blank=True)
    result_url = models.URLField(blank=True)
    thumb_url = models.URLField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS, default="queued")
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Asset#{self.id} {self.status}"
