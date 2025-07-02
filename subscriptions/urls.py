# subscriptions/urls.py
from django.urls import path
from .views import get_welcome_email_template, subscribe

urlpatterns = [
    path("", subscribe),
    path("welcome-template/", get_welcome_email_template),
]
