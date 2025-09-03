from django.urls import path
from . import views

urlpatterns = [
    path("google-login/", views.google_login, name="google-login"),
    path("google-callback/", views.google_callback, name="google-callback"),
    path("ads-data/", views.ads_data, name="ads-data"),
    path("exchange-code/", views.exchange_code, name="exchange-code"),
]
