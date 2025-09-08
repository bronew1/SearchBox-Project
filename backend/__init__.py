try:
    from .celery import app as celery_app
except ImportError:
    # Render gibi src yapısında sorun olursa fallback
    import importlib
    celery_app = importlib.import_module("backend.celery").app

__all__ = ("celery_app",)
