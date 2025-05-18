from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

def health_check(request):
    return HttpResponse("ok")

urlpatterns = [
    path('', lambda request: HttpResponse("Welcome to SearchBox API")),  # geçici test
    path('admin/', admin.site.urls),
    path('api/product/', include('products.urls')),
    path('api/recommendations', include('recommendations.urls')),
    path("api/ga4/", include("analytics.urls")),
    path("healthz", health_check),
    path("api/", include("analytics.urls")),
]
