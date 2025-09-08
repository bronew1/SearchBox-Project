import os
import ssl
from celery import Celery

app = Celery("backend")

# Ortak ayarlar
app.conf.broker_url = os.getenv("CELERY_BROKER_URL")
app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")

# SSL ayarları (rediss:// için gerekli)
app.conf.broker_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE
}
app.conf.redis_backend_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE
}
