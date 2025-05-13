# recommendations/urls.py
from django.urls import path
from .views import trending_products

urlpatterns = [
    #path('', get_recommendations, name='get_recommendations'),
   # path('import-ga4/', import_from_ga4, name='import_from_ga4'),
    path('trending/', trending_products, name='trending_products'),
]
