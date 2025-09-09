import os
import ssl
from celery import Celery

app = Celery("backend")

app.conf.update(
    broker_url=os.getenv("CELERY_BROKER_URL"),
    result_backend=os.getenv("CELERY_RESULT_BACKEND"),
)

app.autodiscover_tasks()
