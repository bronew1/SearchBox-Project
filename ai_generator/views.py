import requests
import os
import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

@api_view(['POST'])
def generate_image(request):
    prompt = request.data.get("prompt")
    aspect_ratio = request.data.get("aspect_ratio", "1:1")  # Örn: 1:1, 16:9, 9:16

    if not prompt:
        return Response({"error": "Prompt is required"}, status=400)

    url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    headers = {
        "Authorization": f"Bearer {settings.STABILITY_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {
        "prompt": prompt,
        "output_format": "png",
        "aspect_ratio": aspect_ratio
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        image_url = response.json().get("image")
        local_path = save_image_from_url(image_url)
        return Response({"image_url": local_path})
    except Exception as e:
        return Response({"error": str(e)}, status=500)


def save_image_from_url(image_url):
    response = requests.get(image_url)
    filename = f"generated_{int(time.time())}.png"
    path = f"media/ai/{filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "wb") as f:
        f.write(response.content)

    return f"/media/ai/{filename}"
