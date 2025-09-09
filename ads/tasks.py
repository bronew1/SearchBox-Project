# ads/tasks.py
import io
import uuid
import requests
from PIL import Image
from django.conf import settings
from boto3.session import Session
from .models import GeneratedAsset
from backend.celery import app

STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

# ads/tasks.py
@app.task
def generate_ad_task(asset_id: int):
    try:
        asset = GeneratedAsset.objects.get(id=asset_id)
        asset.status = "processing"
        asset.save(update_fields=["status"])

        STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

        headers = {
            "Authorization": f"Bearer {settings.STABILITY_API_KEY}",
            "Accept": "image/*",        # <— ÖNEMLİ: görseli bayt olarak iste
        }
        files = {
            "prompt": (None, asset.prompt),
            "output_format": (None, "png"),
            "aspect_ratio": (None, asset.size or "1:1"),
        }

        resp = requests.post(STABILITY_URL, headers=headers, files=files, timeout=60)

        # Yanıtın gerçekten image olup olmadığını kontrol et
        ct = resp.headers.get("content-type", "")
        if resp.status_code != 200 or not ct.startswith("image/"):
            asset.status = "failed"
            asset.error = f"Stability error ({resp.status_code}): {resp.text[:300]}"
            asset.save(update_fields=["status", "error"])
            return

        image_bytes = io.BytesIO(resp.content)
        Image.open(image_bytes)  # basit validasyon

        # Cloudflare R2 yüklemesi
        filename = f"ads/{uuid.uuid4()}.png"
        bucket.upload_fileobj(io.BytesIO(resp.content), filename, ExtraArgs={"ContentType": "image/png"})
        file_url = f"{settings.R2['endpoint_url']}/{settings.R2['bucket']}/{filename}"

        asset.status = "completed"
        asset.result_url = file_url
        asset.thumb_url = file_url
        asset.save(update_fields=["status", "result_url", "thumb_url"])

    except Exception as e:
        # güvenli hata yakalama
        asset = GeneratedAsset.objects.get(id=asset_id)
        asset.status = "failed"
        asset.error = str(e)
        asset.save(update_fields=["status", "error"])
