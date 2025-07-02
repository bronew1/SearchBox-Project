# subscriptions/urls.py
from django.urls import path
from .views import get_welcome_email_template, subscribe, update_welcome_email_template

urlpatterns = [
    path("", subscribe),
    path("welcome-template/", get_welcome_email_template),
     path("welcome-template/update/", update_welcome_email_template),
]
