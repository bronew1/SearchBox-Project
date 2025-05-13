from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/product/', include('products.urls')),
    path('api/', include('recommendations.urls')),
    path("api/ga4/", include("analytics.urls")),
]
