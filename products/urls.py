from django.urls import path
from .views import upload_xml

urlpatterns = [
    path("upload-xml/", upload_xml, name="upload-xml"),
]
