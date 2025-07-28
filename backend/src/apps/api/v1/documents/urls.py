from django.urls import path

from apps.api.v1.documents.views import DocumentUploadView, DocumentListView


urlpatterns = [
    path(
        "",
        DocumentListView.as_view(),
        name="api-v1-document-list",
    ),
    path(
        "/upload",
        DocumentUploadView.as_view(),
        name="api-v1-document-upload",
    ),
]
