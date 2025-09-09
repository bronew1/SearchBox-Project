# ads/tasks.py
import io
import uuid
import requests
from PIL import Image
from django.conf import settings
from boto3.session import Session
from celery import shared_task

STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

@shared_task(name="ads.tasks.generate_ad_task")
def _get_r2_bucket():
    """R2 bağlantısını çalışma anında kur (import-time değil)."""
    session = Session(
        aws_access_key_id=settings.R2["aws_access_key_id"],
        aws_secret_access_key=settings.R2["aws_secret_access_key"],
    )
    s3 = session.resource("s3", endpoint_url=settings.R2["endpoint_url"])
    return s3.Bucket(settings.R2["bucket"])

@shared_task(name="ads.tasks.generate_ad_task")
def generate_ad_task(asset_id: int):
    from .models import GeneratedAsset  # local import: circular riskini azaltır
    asset = None
    try:
        asset = GeneratedAsset.objects.get(id=asset_id)
        asset.status = "processing"
        asset.save(update_fields=["status"])

        # Stability API - binary çıktı iste
        headers = {
            "Authorization": f"Bearer {settings.STABILITY_API_KEY}",
            "Accept": "image/*",
        }
        files = {
            "prompt": (None, asset.prompt or ""),
            "output_format": (None, "png"),
            "aspect_ratio": (None, asset.size or "1:1"),
        }

        resp = requests.post(STABILITY_URL, headers=headers, files=files, timeout=90)

        if resp.status_code != 200:
            asset.status = "failed"
            # JSON döndüyse okunabilir hata yaz
            try:
                asset.error = resp.json()
            except Exception:
                asset.error = resp.text
            asset.save(update_fields=["status", "error"])
            return

        # Görsel doğrula
        img_bytes = io.BytesIO(resp.content)
        Image.open(img_bytes)  # sadece validasyon

        # R2'ya yükle
        bucket = _get_r2_bucket()
        key = f"ads/{uuid.uuid4()}.png"
        bucket.upload_fileobj(io.BytesIO(resp.content), key, ExtraArgs={"ContentType": "image/png"})

        url = f"{settings.R2['endpoint_url']}/{settings.R2['bucket']}/{key}"

        asset.status = "completed"
        asset.result_url = url
        asset.thumb_url = url
        asset.save(update_fields=["status", "result_url", "thumb_url"])

    except Exception as e:
        if asset is None:
            # asset bulunamadıysa dahi logla (opsiyonel: Sentry vs.)
            return
        asset.status = "failed"
        asset.error = str(e)
        asset.save(update_fields=["status", "error"])

@shared_task(name="ads.tasks.debug_task")
def debug_task():
    print("✅ Celery çalışıyor!")
    return "done"
