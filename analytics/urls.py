from django.urls import path
from .views import search_terms_view

urlpatterns = [
    path("search-terms/", search_terms_view, name="search-terms"),
    
]
