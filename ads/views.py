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
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=["https://www.googleapis.com/auth/adwords"],
    )
    flow.redirect_uri = settings.GOOGLE_ADS["redirect_uri"]
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",   # ilk sefer refresh token garantisi için
    )
    request.session["gads_oauth_state"] = state
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
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
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
    email = None  # istersen id_token içinden email çıkarabilirsin

    conn = GoogleAdsConnection.objects.create(
        email=email, refresh_token=refresh_token, login_customer_id=settings.GOOGLE_ADS.get("login_customer_id")
    )

    # Bağlı hesapları ekle
    for cid in list_accessible_customers(refresh_token):
        meta = get_customer_metadata(refresh_token, cid)
        GoogleAdsAccount.objects.update_or_create(
            connection=conn, customer_id=cid,
            defaults={
                "descriptive_name": meta.get("descriptive_name"),
                "currency_code": meta.get("currency_code"),
            }
        )
    # Frontend'e döneceğin bir sayfa varsa oraya yönlendir
    return HttpResponse("Google Ads hesabı bağlandı. Pencereyi kapatıp panele dönebilirsiniz ✅")

def list_accounts(request):
    # basit: son bağlantıyı kullan
    conn = GoogleAdsConnection.objects.order_by("-id").first()
    if not conn:
        return JsonResponse({"connected": False, "accounts": []})
    accs = [
        {
            "id": a.id,
            "customer_id": a.customer_id,
            "name": a.descriptive_name,
            "currency": a.currency_code,
        } for a in GoogleAdsAccount.objects.filter(connection=conn).order_by("descriptive_name")
    ]
    return JsonResponse({"connected": True, "accounts": accs})

@csrf_exempt
def sync_campaign_daily_view(request):
    """POST: {customer_id, start?, end?} -> DB'ye yazar"""
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    conn = GoogleAdsConnection.objects.order_by("-id").first()
    if not conn:
        return HttpResponseBadRequest("No connection")

    import json
    body = json.loads(request.body or "{}")
    customer_id = body.get("customer_id")
    if not customer_id:
        return HttpResponseBadRequest("customer_id is required")

    start_s = body.get("start")
    end_s = body.get("end")
    end = datetime.strptime(end_s, "%Y-%m-%d").date() if end_s else (date.today() - timedelta(days=1))
    start = datetime.strptime(start_s, "%Y-%m-%d").date() if start_s else (end - timedelta(days=29))

    account = GoogleAdsAccount.objects.get(customer_id=customer_id)
    created_rows = 0

    stream = stream_campaign_daily(conn.refresh_token, customer_id, start, end)
    bulk = []
    for batch in stream:
        for r in batch.results:
            bulk.append(AdMetricDaily(
                account=account,
                campaign_id=str(r.campaign.id),
                campaign_name=r.campaign.name,
                date=r.segments.date.value,
                impressions=int(r.metrics.impressions or 0),
                clicks=int(r.metrics.clicks or 0),
                cost=(r.metrics.cost_micros or 0)/1_000_000,
                conversions=float(r.metrics.conversions or 0),
                revenue=float(r.metrics.conversions_value or 0),
            ))
            if len(bulk) >= 1000:
                AdMetricDaily.objects.bulk_create(bulk, ignore_conflicts=True)
                created_rows += len(bulk)
                bulk = []
    if bulk:
        AdMetricDaily.objects.bulk_create(bulk, ignore_conflicts=True)
        created_rows += len(bulk)

    return JsonResponse({"status": "ok", "inserted": created_rows, "start": start.isoformat(), "end": end.isoformat()})

def metrics_table(request):
    """GET ?customer_id=...&start=YYYY-MM-DD&end=YYYY-MM-DD"""
    customer_id = request.GET.get("customer_id")
    if not customer_id:
        return HttpResponseBadRequest("customer_id required")
    start = request.GET.get("start")
    end = request.GET.get("end")
    qs = AdMetricDaily.objects.filter(account__customer_id=customer_id)
    if start: qs = qs.filter(date__gte=start)
    if end:   qs = qs.filter(date__lte=end)
    # kampanya-gün kırılımı
    data = list(qs.order_by("-date", "campaign_name").values(
        "date", "campaign_id", "campaign_name", "impressions", "clicks", "cost", "conversions", "revenue"
    ))
    # toplamlar
    tot = {"impressions": 0, "clicks": 0, "cost": 0.0, "revenue": 0.0}
    for r in data:
        tot["impressions"] += r["impressions"]
        tot["clicks"] += r["clicks"]
        tot["cost"] += float(r["cost"])
        tot["revenue"] += float(r["revenue"])
    roas = (tot["revenue"] / tot["cost"]) if tot["cost"] else None
    return JsonResponse({"rows": data, "summary": {**tot, "roas": roas}})
