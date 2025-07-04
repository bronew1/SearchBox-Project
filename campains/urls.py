from django.urls import path
from .views import create_campaign, list_campaigns

urlpatterns = [
     path("", list_campaigns, name="list_campaigns"),  # Listeleme
    path("create/", create_campaign, name="create_campaign"),  
]
