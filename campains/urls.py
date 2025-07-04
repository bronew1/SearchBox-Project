# campaigns/urls.py
from django.urls import path
from .views import create_campaign

urlpatterns = [
    path("create/", create_campaign, name="create_campaign"),
]
