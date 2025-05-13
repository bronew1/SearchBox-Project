# recommendations/urls.py
from django.urls import path
from .views import trending_products, health_check

urlpatterns = [
    #path('', get_recommendations, name='get_recommendations'),
   # path('import-ga4/', import_from_ga4, name='import_from_ga4'),
    path('trending/', trending_products, name='trending_products'),
    path('', health_check, name='health_check'),

]
