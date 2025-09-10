from django.urls import path
from .views import GenerateAd, JobStatus, AssetList
from . import views

urlpatterns = [
    path("generate-ad/", GenerateAd.as_view(), name="generate-ad"),
    path("jobs/<int:pk>/", JobStatus.as_view(), name="job-status"),
    path("assets/", AssetList.as_view(), name="asset-list"),
    path("google-auth/", views.google_auth_start, name="google_auth_start"),
    path("oauth2callback/", views.google_auth_callback, name="google_auth_callback"),
    path("api/ads/accounts/", views.list_accounts, name="ads_accounts"),
    path("api/ads/sync/", views.sync_campaign_daily_view, name="ads_sync"),
    path("api/ads/metrics/", views.metrics_table, name="ads_metrics"),
]




 #path("google-login/", views.google_login, name="google-login"),
    #path("google-callback/", views.google_callback, name="google-callback"),
    #path("ads-data/", views.ads_data, name="ads-data"),
    #path("exchange-code/", views.exchange_code, name="exchange-code"),