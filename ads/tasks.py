# ads/tasks.py
import io
import uuid
import requests
from PIL import Image
from django.conf import settings
from boto3.session import Session
from celery import shared_task
from .models import GeneratedAsset

STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

# Cloudflare R2 client
session = Session(
    aws_access_key_id=settings.R2["aws_access_key_id"],
    aws_secret_access_key=settings.R2["aws_secret_access_key"],
)
s3 = session.resource("s3", endpoint_url=settings.R2["endpoint_url"])
bucket = s3.Bucket(settings.R2["bucket"])


@shared_task(name="ads.tasks.generate_ad_task")
def generate_ad_task(asset_id: int):
    """
    Bir GeneratedAsset kaydı alır, Stability API'den görsel üretir,
    R2'ya yükler ve DB'yi günceller.
    """
    asset = GeneratedAsset.objects.get(id=asset_id)

    try:
        asset.status = "processing"
        asset.save(update_fields=["status"])

        headers = {
            "Authorization": f"Bearer {settings.STABILITY_API_KEY}",
            "Accept": "application/json",
        }
        files = {
            "prompt": (None, asset.prompt or ""),
            "output_format": (None, "png"),
            "aspect_ratio": (None, asset.size or "1:1"),
        }

        # İsteği yap
        resp = requests.post(STABILITY_URL, headers=headers, files=files, timeout=120)

        if resp.status_code != 200:
            asset.status = "failed"
            asset.error = f"stability_error {resp.status_code}: {resp.text[:1000]}"
            asset.save(update_fields=["status", "error"])
            return

        # Görsel doğrulaması
        image_bytes = io.BytesIO(resp.content)
        Image.open(image_bytes)  # hata fırlatırsa except'e düşer

        # R2'ya yükle
        key = f"ads/{uuid.uuid4()}.png"
        bucket.upload_fileobj(
            io.BytesIO(resp.content),
            key,
            ExtraArgs={"ContentType": "image/png"},
        )

        file_url = f"{settings.R2['endpoint_url']}/{settings.R2['bucket']}/{key}"

        asset.status = "completed"
        asset.result_url = file_url
        asset.thumb_url = file_url
        asset.error = ""
        asset.save(update_fields=["status", "result_url", "thumb_url", "error"])

    except Exception as e:
        # Hata durumunu kaydet
        asset.status = "failed"
        asset.error = str(e)[:1000]
        asset.save(update_fields=["status", "error"])


@shared_task(name="ads.tasks.debug_task")
def debug_task():
    print("✅ Celery çalışıyor!")
    return "done"
