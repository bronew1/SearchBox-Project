from django.urls import path
from .views import GenerateAd, JobStatus, AssetList
from . import views

urlpatterns = [
    # Ad Generator
    path("generate-ad/", GenerateAd.as_view(), name="generate-ad"),
    path("jobs/<int:pk>/", JobStatus.as_view(), name="job-status"),
    path("assets/", AssetList.as_view(), name="asset-list"),

    # Google OAuth flow
    path("google-auth/", views.google_auth_start, name="google_auth_start"),
    path("oauth2callback/", views.google_auth_callback, name="google_auth_callback"),
    

    # Google Ads verileri
    path("accounts/", views.list_accounts, name="ads_accounts"),
    path("sync/", views.sync_campaign_daily_view, name="ads_sync"),
    path("metrics/", views.metrics_table, name="ads_metrics"),
]
