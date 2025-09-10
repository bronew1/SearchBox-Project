import os
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY") or settings.STABILITY_API_KEY

@api_view(["POST"])
def generate_image(request):
    prompt = request.data.get("prompt")
    aspect_ratio = request.data.get("aspect_ratio", "1:1")

    if not prompt:
        return Response({"error": "Prompt is required."}, status=400)

    try:
        # Stability API endpoint
        url = "https://api.stability.ai/v2beta/stable-image/generate/core"

        headers = {
            "Authorization": f"Bearer {STABILITY_API_KEY}"
        }

        files = {
            "prompt": (None, prompt),
            "aspect_ratio": (None, aspect_ratio),
        }

        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            image_url = response.json()["image"]
            return Response({"image_url": image_url})
        else:
            return Response({"error": response.text}, status=response.status_code)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
