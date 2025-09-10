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





class GoogleAdsConnection(models.Model):
    # Basit: tek kurulum için user zorunlu kılmıyoruz
    email = models.EmailField(null=True, blank=True)
    refresh_token = models.TextField()
    login_customer_id = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class GoogleAdsAccount(models.Model):
    connection = models.ForeignKey(GoogleAdsConnection, on_delete=models.CASCADE, related_name="accounts")
    customer_id = models.CharField(max_length=20)  # "1234567890"
    descriptive_name = models.CharField(max_length=255, null=True, blank=True)
    currency_code = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        unique_together = [("connection", "customer_id")]

class AdMetricDaily(models.Model):
    account = models.ForeignKey(GoogleAdsAccount, on_delete=models.CASCADE, related_name="daily_metrics")
    campaign_id = models.CharField(max_length=30)
    campaign_name = models.CharField(max_length=255)
    date = models.DateField()
    impressions = models.BigIntegerField(default=0)
    clicks = models.BigIntegerField(default=0)
    cost = models.DecimalField(max_digits=14, decimal_places=6)  # para birimi biriminde
    conversions = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        unique_together = [("account", "campaign_id", "date")]
        indexes = [models.Index(fields=["account", "date"])]
