from django.urls import path
from .views import search_terms_view, track_event

urlpatterns = [
    path("search-terms/", search_terms_view, name="search-terms"),
    path('track-event/', track_event, name='track_event'),
]
