# backend/celery.py
import os
import ssl
from celery import Celery

# Django ayarlarını göster
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")

# Django settings içindeki CELERY_* ile başlayanları otomatik al
app.config_from_object("django.conf:settings", namespace="CELERY")

# Django app'lerindeki tasks.py dosyalarını otomatik tara
app.autodiscover_tasks()

# --- Redis TLS (Render 'rediss://') için güvenli/uyumlu ayar ---
broker_url = os.getenv("CELERY_BROKER_URL", "")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "")

if broker_url.startswith("rediss://"):
    # Sertifika doğrulaması istersen CERT_REQUIRED yapabilirsin
    app.conf.broker_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}

if result_backend.startswith("rediss://"):
    app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}
