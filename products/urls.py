from django.urls import path
from .views import upload_xml, widget_products

urlpatterns = [
    path("upload-xml/", upload_xml, name="upload-xml"),
    path("widget-products/", widget_products, name="widget-products"),
]


