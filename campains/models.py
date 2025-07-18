from django.db import models

SEGMENT_CHOICES = [
    ('cart', 'Sepete Ekleyenler'),
    ('viewers', 'Ürünü Görüntüleyenler'),
    ('members', 'Sadece Üyeler'),
]

PRICE_CONDITION_CHOICES = [
    ('higher', 'Daha yüksek'),
    ('lower', 'Daha düşük'),
]

class EmailCampaign(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True)
    html_content = models.TextField()
    design_json = models.JSONField(null=True, blank=True)  # ✅ YENİ
    segment = models.CharField(max_length=50, blank=True)
    send_after_days = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_template = models.BooleanField(default=False)

    def __str__(self):
        return self.title


    # 💡 Yeni alanlar
    price_limit = models.FloatField(null=True, blank=True)
    price_condition = models.CharField(max_length=20, choices=PRICE_CONDITION_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.title