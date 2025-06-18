from django.contrib import admin

from products.models import WidgetProductSelection

# Register your models here.
@admin.register(WidgetProductSelection)
class WidgetProductSelectionAdmin(admin.ModelAdmin):
    list_display = ["product", "order"]