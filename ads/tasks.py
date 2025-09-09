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

@app.task
def generate_ad_task(asset_id: int):
    asset = GeneratedAsset.objects.get(id=asset_id)
    try:
        asset.status = "processing"
        asset.save(update_fields=["status"])

        # ---- Stability çağrısı ----
        headers = {
            "Authorization": f"Bearer {settings.STABILITY_API_KEY}",
            # 🔴 Görsel bytes istiyoruz
            "Accept": "image/*",
        }
        files = {
            "prompt": (None, asset.prompt or ""),
            "output_format": (None, "png"),
            "aspect_ratio": (None, asset.size or "1:1"),
        }

        resp = requests.post(STABILITY_URL, headers=headers, files=files, timeout=60)

        if resp.status_code != 200:
            asset.status = "failed"
            asset.error = f"Stability error {resp.status_code}: {resp.text[:500]}"
            asset.save(update_fields=["status", "error"])
            return

        # ---- Görsel doğrulama ----
        image_bytes = io.BytesIO(resp.content)
        Image.open(image_bytes)  # sadece validasyon

        # ---- R2 client'ını burada kur ----
        sess = Session(
            aws_access_key_id=settings.R2["aws_access_key_id"],
            aws_secret_access_key=settings.R2["aws_secret_access_key"],
        )
        s3 = sess.resource("s3", endpoint_url=settings.R2["endpoint_url"])

        bucket_name = settings.R2["bucket"]
        if not bucket_name:
            raise ValueError("R2 bucket adı boş!")

        filename = f"ads/{uuid.uuid4()}.png"
        s3.Bucket(bucket_name).upload_fileobj(
            io.BytesIO(resp.content),
            filename,
            ExtraArgs={"ContentType": "image/png"},
        )

        file_url = f"{settings.R2['endpoint_url']}/{bucket_name}/{filename}"

        asset.status = "completed"
        asset.result_url = file_url
        asset.thumb_url = file_url
        asset.save(update_fields=["status", "result_url", "thumb_url"])

    except Exception as e:
        asset.status = "failed"
        asset.error = str(e)
        asset.save(update_fields=["status", "error"])
