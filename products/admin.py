from django.contrib import admin

from products.models import WidgetProduct



# Register your models here.
@admin.register(WidgetProduct)
class WidgetProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "sku", "order"]
    list_editable = ["order"]