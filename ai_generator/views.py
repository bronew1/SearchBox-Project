import openai
import base64
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

openai.api_key = os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY

@api_view(['POST'])
def generate_image(request):
    prompt = request.data.get("prompt")
    width = request.data.get("width", 1024)
    height = request.data.get("height", 1024)

    if not prompt:
        return Response({"error": "Prompt is required"}, status=400)

    try:
        # DALL·E 3 supports only `1024x1024`, `1024x1792`, or `1792x1024`
        size = f"{width}x{height}"

        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            response_format="b64_json"
        )

        image_data = response['data'][0]['b64_json']
        image_url = save_image_to_file(image_data)

        return Response({"image_url": image_url})

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def save_image_to_file(b64_data):
    image_bytes = base64.b64decode(b64_data)
    filename = f"generated_{int(openai.time.time())}.png"
    path = f"media/ai/{filename}"

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "wb") as f:
        f.write(image_bytes)

    return f"/media/ai/{filename}"
