from rest_framework import serializers
from .models import GeneratedAsset

class AssetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedAsset
        fields = ["id","prompt","cta","slogan","url","size","product_image"]

class AssetReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedAsset
        fields = "__all__"
