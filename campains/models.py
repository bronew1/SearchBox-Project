from django.db import models

SEGMENT_CHOICES = [
    ('cart', 'Sepete Ekleyenler'),
    ('viewers', 'Ürünü Görüntüleyenler'),
    ('members', 'Sadece Üyeler'),
]

class EmailCampaign(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    html_content = models.TextField()
    segment = models.CharField(max_length=50, choices=SEGMENT_CHOICES)
    send_after_days = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
