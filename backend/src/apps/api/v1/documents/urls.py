from django.urls import path

from apps.api.v1.documents.views import DocumentUploadView, DocumentListView


urlpatterns = [
    path(
        "",
        DocumentListView.as_view(),
        name="api-v1-documents-list",
    ),
    path(
        "/upload",
        DocumentUploadView.as_view(),
        name="api-v1-documents-upload",
    ),
]
