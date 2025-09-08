from rest_framework import generics
from rest_framework.permissions import AllowAny  # test için
from .models import GeneratedAsset
from .serializers import AssetCreateSerializer, AssetReadSerializer
from .tasks import generate_ad_task


class GenerateAd(generics.CreateAPIView):
    """
    Kullanıcıdan prompt alır, GeneratedAsset kaydı oluşturur
    ve Celery task tetikleyerek görsel üretimini başlatır.
    """
    queryset = GeneratedAsset.objects.all()
    serializer_class = AssetCreateSerializer
    permission_classes = [AllowAny]  # test için serbest

    def perform_create(self, serializer):
        asset = serializer.save()  # şimdilik user eklemedik
        generate_ad_task.delay(asset.id)


class JobStatus(generics.RetrieveAPIView):
    """
    Tek bir job'un durumunu (queued, processing, completed, failed) döner.
    """
    queryset = GeneratedAsset.objects.all()
    serializer_class = AssetReadSerializer
    permission_classes = [AllowAny]  # test için serbest


class AssetList(generics.ListAPIView):
    """
    Tüm oluşturulmuş asset’leri listeler.
    """
    queryset = GeneratedAsset.objects.all().order_by("-created_at")
    serializer_class = AssetReadSerializer
    permission_classes = [AllowAny]  # test için serbest
