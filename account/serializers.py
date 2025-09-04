from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class AdminOnlyTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_staff:
            raise serializers.ValidationError("Yalnızca admin kullanıcıları giriş yapabilir")
        return data
