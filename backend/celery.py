# backend/celery.py
import os, ssl
from celery import Celery

app = Celery("backend")

broker_url = os.getenv("CELERY_BROKER_URL")
result_backend = os.getenv("CELERY_RESULT_BACKEND")

app.conf.update(broker_url=broker_url, result_backend=result_backend)

if broker_url and broker_url.startswith("rediss://"):
    app.conf.broker_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}
if result_backend and result_backend.startswith("rediss://"):
    app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}

app.autodiscover_tasks()
