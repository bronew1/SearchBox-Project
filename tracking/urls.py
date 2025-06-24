 
from django.urls import path
from .views import track_event, cart_count, daily_add_to_cart_stats

urlpatterns = [
    path('daily-add-to-cart-stats/', daily_add_to_cart_stats, name='daily_add_to_cart_stats'),
]
