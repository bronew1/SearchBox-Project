# backend/celery.py
import os
from celery import Celery

# 🔴 Django ayarlarını yükle
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")

# 🔴 Django settings üzerinden CELERY_* okumayı aç
app.config_from_object("django.conf:settings", namespace="CELERY")

# 🔴 Tüm apps içindeki tasks.py’leri tara
app.autodiscover_tasks()
