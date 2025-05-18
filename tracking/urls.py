# tracking/urls.py
from django.urls import path
from .views import track_event

urlpatterns = [
    path("track-event/", track_event),
]
