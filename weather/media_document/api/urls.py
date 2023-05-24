from django.urls import path
from . import views

app_name = "media_document"


urlpatterns = [
    path("", views.DocumentUploadView.as_view(), name="handler-document-upload"),
]
