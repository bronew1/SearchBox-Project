from rest_framework import generics
from rest_framework.permissions import AllowAny  # test için
from .models import GeneratedAsset
from .serializers import AssetCreateSerializer, AssetReadSerializer
from .tasks import generate_ad_task
from datetime import date, timedelta, datetime
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from google_auth_oauthlib.flow import Flow
from .models import GoogleAdsConnection, GoogleAdsAccount, AdMetricDaily
from .services.google_ads import list_accessible_customers, get_customer_metadata, stream_campaign_daily



class GenerateAd(generics.CreateAPIView):
    """
    Kullanıcıdan prompt alır, GeneratedAsset kaydı oluşturur
    ve Celery task tetikleyerek görsel üretimini başlatır.
    """
    queryset = GeneratedAsset.objects.all()
    serializer_class = AssetCreateSerializer
    permission_classes = [AllowAny]  # test için serbest

    def perform_create(self, serializer):
        asset = serializer.save()  # şimdilik user eklemedik
        generate_ad_task.delay(asset.id)


class JobStatus(generics.RetrieveAPIView):
    """
    Tek bir job'un durumunu (queued, processing, completed, failed) döner.
    """
    queryset = GeneratedAsset.objects.all()
    serializer_class = AssetReadSerializer
    permission_classes = [AllowAny]  # test için serbest


class AssetList(generics.ListAPIView):
    """
    Tüm oluşturulmuş asset’leri listeler.
    """
    queryset = GeneratedAsset.objects.all().order_by("-created_at")
    serializer_class = AssetReadSerializer
    permission_classes = [AllowAny]  # test için serbest



def google_auth_start(request):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_ADS["client_id"],
                "client_secret": settings.GOOGLE_ADS["client_secret"],
                "redirect_uris": [settings.GOOGLE_ADS["redirect_uri"]],
                "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",   # ✅ güncel endpoint
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=["https://www.googleapis.com/auth/adwords"],
    )
    flow.redirect_uri = settings.GOOGLE_ADS["redirect_uri"]
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    request.session["gads_oauth_state"] = state
    print("👉 Redirect URI being sent:", flow.redirect_uri)  # Debug
    return redirect(auth_url)


def google_auth_callback(request):
    state = request.session.get("gads_oauth_state")
    if not state:
        return HttpResponseBadRequest("State missing")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_ADS["client_id"],
                "client_secret": settings.GOOGLE_ADS["client_secret"],
                "redirect_uris": [settings.GOOGLE_ADS["redirect_uri"]],
                "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",  # ✅ güncel endpoint
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=["https://www.googleapis.com/auth/adwords"],
        state=state,
    )
    flow.redirect_uri = settings.GOOGLE_ADS["redirect_uri"]

    flow.fetch_token(authorization_response=request.build_absolute_uri())
    creds = flow.credentials

    refresh_token = creds.refresh_token
    email = None

    conn = GoogleAdsConnection.objects.create(
        email=email,
        refresh_token=refresh_token,
        login_customer_id=settings.GOOGLE_ADS.get("login_customer_id"),
    )

    for cid in list_accessible_customers(refresh_token):
        meta = get_customer_metadata(refresh_token, cid)
        GoogleAdsAccount.objects.update_or_create(
            connection=conn, customer_id=cid,
            defaults={
                "descriptive_name": meta.get("descriptive_name"),
                "currency_code": meta.get("currency_code"),
            }
        )
    return HttpResponse("Google Ads hesabı bağlandı ✅ Pencereyi kapatıp panele dönebilirsiniz.")
