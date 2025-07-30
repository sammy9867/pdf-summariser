from django.urls import path

from apps.api.v1.documents.views import (
    DocumentListView,
    DocumentUploadView,
    document_stream_view,
)


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
    path(
        "/<uuid:document_uuid>/stream",
        document_stream_view,
        name="api-v1-document-summaries-stream",
    ),
]
