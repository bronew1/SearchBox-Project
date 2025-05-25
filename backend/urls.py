from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from tracking.views import track_event


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
    path('api/search/', include('search.urls')),
    
]
