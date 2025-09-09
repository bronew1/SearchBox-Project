import os
import ssl
from celery import Celery

# Django ayarlarını Celery başlamadan önce yükle
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")

# Django settings içindeki CELERY_* değerlerini oku (opsiyonel ama iyi pratik)
app.config_from_object("django.conf:settings", namespace="CELERY")

# Render Redis (TLS) kullanıyorsan SSL'i Celery'ye anlat
broker_url = os.getenv("CELERY_BROKER_URL")
result_backend = os.getenv("CELERY_RESULT_BACKEND")

app.conf.update(
    broker_url=broker_url,
    result_backend=result_backend,
)

# rediss:// kullanıyorsan (TLS), sertifika kontrolünü gevşetmek için:
if broker_url and broker_url.startswith("rediss://"):
    app.conf.broker_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}
if result_backend and result_backend.startswith("rediss://"):
    app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}

# Django’daki tüm app’lerin tasks.py dosyalarını otomatik bul
app.autodiscover_tasks()
