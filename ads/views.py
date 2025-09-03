import os
import json
import requests
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from django.views import View
from google.oauth2.credentials import Credentials
from google.ads.googleads.client import GoogleAdsClient
import logging
logger = logging.getLogger(__name__)
from rest_framework.response import Response
from rest_framework.decorators import api_view
# -----------------------------
# Google OAuth yönlendirme
# -----------------------------
def google_login(request):
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/adwords",
        "access_type": "offline",
        "prompt": "consent",
    }
    url = f"{auth_url}?{requests.compat.urlencode(params)}"
    return redirect(url)

# -----------------------------
# Callback
# -----------------------------
def google_callback(request):
    code = request.GET.get("code")
    logger.info(f"Callback called with code: {code}")

    if not code:
        logger.error("No code provided in callback")
        return JsonResponse({"error": "Authorization code not provided"}, status=400)

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(token_url, data=data)
        logger.info(f"Token request status: {response.status_code}")
        response.raise_for_status()
        token_data = response.json()
        logger.info(f"Token data received: {token_data}")

    except requests.exceptions.RequestException as e:
        logger.exception("Failed to fetch access token")
        return JsonResponse({"error": "Token fetch failed", "details": str(e)}, status=500)

    if "access_token" not in token_data:
        logger.error(f"No access token in response: {token_data}")
        return JsonResponse({"error": "No access token in token response", "details": token_data}, status=400)

    # Session’a kaydet
    request.session["google_access_token"] = token_data["access_token"]
    logger.info("Access token saved in session")

    # Frontend’e yönlendir
    return redirect("http://localhost:3000/reklamlar")

# -----------------------------
# Ads verisi endpoint
# -----------------------------
def ads_data(request):
    access_token = request.session.get("google_access_token")
    if not access_token:
        return JsonResponse({"error": "Google hesabına bağlanılmamış"}, status=401)

    try:
        client = GoogleAdsClient.load_from_storage("google-ads.yaml")
        service = client.get_service("GoogleAdsService")

        query = """
            SELECT
              campaign.id,
              campaign.name,
              metrics.clicks,
              metrics.impressions,
              metrics.conversions,
              metrics.cost_micros
            FROM campaign
            WHERE segments.date DURING LAST_7_DAYS
            ORDER BY metrics.impressions DESC
            LIMIT 20
        """

        response = service.search(customer_id="1234567890", query=query)  # Sina Pırlanta Customer ID
        results = []
        for row in response:
            results.append({
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name,
                "clicks": row.metrics.clicks,
                "impressions": row.metrics.impressions,
                "conversions": row.metrics.conversions,
                "cost": row.metrics.cost_micros / 1_000_000
            })

        return JsonResponse({"status": "success", "data": results})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@api_view(["POST"])
def exchange_code(request):
    code = request.data.get("code")
    if not code:
        return Response({"error": "Code not provided"}, status=400)

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        r = requests.post(token_url, data=data)
        r.raise_for_status()
        tokens = r.json()
        return Response(tokens)
    except requests.HTTPError as e:
        return Response({"error": str(e), "details": r.text}, status=400)
