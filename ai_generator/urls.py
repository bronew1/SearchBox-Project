from django.urls import path
from .views import generate_image

urlpatterns = [
    path("generate-image/", generate_image),
]
