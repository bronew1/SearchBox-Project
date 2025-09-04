from django.urls import path
from .views import AdminOnlyTokenView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("token/", AdminOnlyTokenView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
