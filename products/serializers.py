from rest_framework import serializers
from .models import WidgetProduct

class WidgetProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WidgetProduct
        fields = '__all__'