# recommendations/urls.py
from django.urls import path
from .views import get_recommendations, similar_products, trending_products

urlpatterns = [
    #path('', get_recommendations, name='get_recommendations'),
   # path('import-ga4/', import_from_ga4, name='import_from_ga4'),
    path('trending/', trending_products, name='trending_products'),
    path("", get_recommendations, name="get_recommendations"),
    path('similar/<str:sku>/', similar_products, name='similar_products'), 
    


]
