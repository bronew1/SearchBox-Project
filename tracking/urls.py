from django.urls import path
from tracking.views import track_event

urlpatterns = [
    path('track-event/', track_event, name='track-event')
]
