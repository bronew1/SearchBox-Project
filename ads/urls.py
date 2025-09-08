from django.urls import path
from .views import GenerateAd, JobStatus, AssetList

urlpatterns = [
    path("generate-ad/", GenerateAd.as_view(), name="generate-ad"),
    path("jobs/<int:pk>/", JobStatus.as_view(), name="job-status"),
    path("assets/", AssetList.as_view(), name="asset-list"),
]




 #path("google-login/", views.google_login, name="google-login"),
    #path("google-callback/", views.google_callback, name="google-callback"),
    #path("ads-data/", views.ads_data, name="ads-data"),
    #path("exchange-code/", views.exchange_code, name="exchange-code"),