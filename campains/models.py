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

SUBSCRIBER_TIME_CHOICES = [
    ('all', 'Tüm Aboneler'),
    ('1d', 'Son 1 Gün'),
    ('3d', 'Son 3 Gün'),
    ('7d', 'Son 7 Gün'),
    ('30d', 'Son 30 Gün'),
    ('custom', 'Özel Tarih Aralığı'),
]

class EmailCampaign(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True)
    html_content = models.TextField()
    design_json = models.JSONField(null=True, blank=True)
    segment = models.CharField(max_length=50, blank=True)
    send_after_days = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_template = models.BooleanField(default=False)

    # 💡 Yeni alanlar
    price_limit = models.FloatField(null=True, blank=True)
    price_condition = models.CharField(
        max_length=20,
        choices=PRICE_CONDITION_CHOICES,
        null=True,
        blank=True
    )

    # ✅ Zaman aralığı filtresi (abonelik tarihi için)
    subscriber_time_filter = models.CharField(
        max_length=20,
        choices=SUBSCRIBER_TIME_CHOICES,
        default='all'
    )
    custom_start_date = models.DateField(null=True, blank=True)
    custom_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
