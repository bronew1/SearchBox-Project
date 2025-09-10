from django.contrib import admin

# Register your models here.
from .models import GoogleAdsConnection, GoogleAdsAccount, AdMetricDaily

admin.site.register(GoogleAdsConnection)
admin.site.register(GoogleAdsAccount)
admin.site.register(AdMetricDaily)