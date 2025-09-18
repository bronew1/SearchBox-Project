from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from products.views import widget_products
from tracking.views import also_viewed_products, daily_add_to_cart_counts, dashboard_stats, most_viewed_products, revenue_view, user_events_list  # ✔️ Doğru
from tracking.views import cart_count, service_worker, track_event
from subscriptions.views import subscribe 
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



def health_check(request):
    return HttpResponse("ok")

urlpatterns = [
    path('', lambda request: HttpResponse("Search")),  # geçici test
    path('admin/', admin.site.urls),
    path('api/product/', include('products.urls')),
    path('api/recommendations/', include('recommendations.urls')),
    path("api/ga4/", include("analytics.urls")),
    path("healthz", health_check),
    path("api/track-event/", track_event, name="track_event"),
    path("api/revenue/", revenue_view, name="revenue_view"), #ciro
    path('api/subscribe/', include('subscriptions.urls')),
    path("api/cart-count/<str:product_id>/", cart_count),
    path('service-worker.js', service_worker),
    path("api/daily-add-to-cart/", daily_add_to_cart_counts, name="daily_add_to_cart"),
    path("api/user-events/", user_events_list, name="user_events_list"),
    path("api/dashboard-stats/", dashboard_stats, name="dashboard_stats"),
    path("api/most-viewed-products/", most_viewed_products, name="most_viewed_products"),
    path("api/widget-products/", widget_products, name="widget-products"),
    path("widget-products/<int:id>/", widget_products, name="widget-products-detail"),
    path("api/campains/", include("campains.urls")),
    path("api/also-viewed/<str:product_id>/", also_viewed_products, name="also_viewed_products"),
    path("webpush/", include("webPush.urls")),
    path("api/", include("ai_generator.urls")),
    path("api/ads/", include("ads.urls")),
    path("api/accounts/", include("account.urls")),  
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/ai/", include("ai.urls")),
    
]


    
   # path("api/", include("products.urls")),
    
    


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#