import io
import uuid
import requests
from PIL import Image
from django.conf import settings
from boto3.session import Session
from .models import GeneratedAsset
from backend.celery import app

# Stability AI endpoint
STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

# Cloudflare R2 session
session = Session(
    aws_access_key_id=settings.R2["aws_access_key_id"],
    aws_secret_access_key=settings.R2["aws_secret_access_key"],
)
s3 = session.resource("s3", endpoint_url=settings.R2["endpoint_url"])
bucket = s3.Bucket(settings.R2["bucket"])


@app.task
def generate_ad_task(asset_id: int):
    try:
        asset = GeneratedAsset.objects.get(id=asset_id)
        asset.status = "processing"
        asset.save(update_fields=["status"])

        # Stability API çağrısı
        headers = {
            "Authorization": f"Bearer {settings.STABILITY_API_KEY}",
            "Accept": "application/json",  # 🔑 önemli

        }

        files = {
            "prompt": (None, asset.prompt),
            "output_format": (None, "png"),
            "aspect_ratio": (None, asset.size if asset.size else "1:1"),
        }

        response = requests.post(STABILITY_URL, headers=headers, files=files)

        if response.status_code != 200:
            asset.status = "failed"
            asset.error = response.text
            asset.save(update_fields=["status", "error"])
            return

        # Görseli oku
        image_bytes = io.BytesIO(response.content)
        Image.open(image_bytes)  # sadece validasyon için

        # R2'ya yükle
        filename = f"ads/{uuid.uuid4()}.png"
        bucket.upload_fileobj(
            io.BytesIO(response.content),
            filename,
            ExtraArgs={"ContentType": "image/png"}
        )

        file_url = f"{settings.R2['endpoint_url']}/{settings.R2['bucket']}/{filename}"

        # DB güncelle
        asset.status = "completed"
        asset.result_url = file_url
        asset.thumb_url = file_url
        asset.save(update_fields=["status", "result_url", "thumb_url"])

    except Exception as e:
        asset = GeneratedAsset.objects.get(id=asset_id)
        asset.status = "failed"
        asset.error = str(e)
        asset.save(update_fields=["status", "error"])


@app.task
def debug_task():
    print("✅ Celery çalışıyor!")
    return "done"
