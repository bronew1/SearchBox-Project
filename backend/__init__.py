# backend/__init__.py
from .celery import app as celery_app  # Celery app'i Django import edilince yüklensin

__all__ = ["celery_app"]
