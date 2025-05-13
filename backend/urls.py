from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include



urlpatterns = [
    path('', lambda request: HttpResponse("Welcome to SearchBox API")),  # geçici test
    path('admin/', admin.site.urls),
    path('api/product/', include('products.urls')),
    path('api/', include('recommendations.urls')),
    path("api/ga4/", include("analytics.urls")),
    path("healthz", include("recommendations.urls")),
]
