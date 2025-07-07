from django.urls import path
from .views import campaign_detail, create_campaign, delete_campaign, list_campaigns

urlpatterns = [
    path("", list_campaigns, name="list_campaigns"), 
    path("create/", create_campaign, name="create_campaign"),  
    path("<int:pk>/", campaign_detail, name="campaign_detail"),
    path("delete/<int:pk>/", delete_campaign, name="delete_campaign"),
]

#