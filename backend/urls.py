from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from tracking.views import cart_count, track_event
from subscriptions.views import subscribe 
from django.conf import settings
from django.conf.urls.static import static


def health_check(request):
    return HttpResponse("ok")

urlpatterns = [
    path('', lambda request: HttpResponse("Search")),  # geçici test
    path('admin/', admin.site.urls),
    path('api/product/', include('products.urls')),
    path('api/recommendations/', include('recommendations.urls')),
    path("api/ga4", include("analytics.urls")),
    path("healthz", health_check),
    path("api/track-event/", track_event, name="track_event"),
    path('api/subscribe/', subscribe),
    path("api/cart-count/<str:product_id>/", cart_count),
   # path("api/", include("products.urls")),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
