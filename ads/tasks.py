# ads/tasks.py
import io, uuid, logging, requests
from PIL import Image
from django.conf import settings
from boto3.session import Session
from .models import GeneratedAsset
from backend.celery import app

log = logging.getLogger(__name__)

STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

def _r2_bucket():
    # Bucket/Session'i import anında değil, task içinde kur
    session = Session(
        aws_access_key_id=settings.R2["aws_access_key_id"],
        aws_secret_access_key=settings.R2["aws_secret_access_key"],
    )
    s3 = session.resource("s3", endpoint_url=settings.R2["endpoint_url"])
    return s3.Bucket(settings.R2["bucket"])

@app.task(bind=True)
def generate_ad_task(self, asset_id: int):
    try:
        asset = GeneratedAsset.objects.get(id=asset_id)
        asset.status = "processing"
        asset.save(update_fields=["status"])

        headers = {
            "Authorization": f"Bearer {settings.STABILITY_API_KEY}",
            # ✅ Görsel döndürmesi için JSON değil image/* istemeliyiz
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
            asset.error = f"{resp.status_code} {resp.text[:500]}"
            asset.save(update_fields=["status", "error"])
            log.error("Stability fail: %s %s", resp.status_code, resp.text)
            return

        # İçerik gerçekten PNG mi doğrula
        img_bytes = io.BytesIO(resp.content)
        Image.open(img_bytes)  # doğrulama

        bucket = _r2_bucket()
        key = f"ads/{uuid.uuid4()}.png"
        bucket.upload_fileobj(io.BytesIO(resp.content), key,
                              ExtraArgs={"ContentType": "image/png"})

        file_url = f"{settings.R2['endpoint_url']}/{settings.R2['bucket']}/{key}"

        asset.status = "completed"
        asset.result_url = file_url
        asset.thumb_url = file_url
        asset.save(update_fields=["status", "result_url", "thumb_url"])

    except Exception as e:
        log.exception("generate_ad_task error")
        try:
            asset = GeneratedAsset.objects.get(id=asset_id)
            asset.status = "failed"
            asset.error = str(e)
            asset.save(update_fields=["status", "error"])
        except Exception:
            pass  # en kötü durumda log yeter
