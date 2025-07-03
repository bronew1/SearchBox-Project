from django.urls import path
from .views import revenue_view, search_terms_view


urlpatterns = [
    path("search-terms/", search_terms_view, name="search-terms"),
    path("revenue/", revenue_view, name="revenue"),
]
