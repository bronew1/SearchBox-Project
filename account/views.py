from rest_framework_simplejwt.views import TokenViewBase
from .serializers import AdminOnlyTokenSerializer

class AdminOnlyTokenView(TokenViewBase):
    serializer_class = AdminOnlyTokenSerializer
