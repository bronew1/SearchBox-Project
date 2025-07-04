from django.urls import path
from .views import create_campaign, list_campaigns

urlpatterns = [
    path("create/", create_campaign, name="create_campaign"),
    path("list/", list_campaigns, name="list_campaigns"),
]
