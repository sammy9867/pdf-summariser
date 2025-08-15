from django.urls import path

from apps.api.v1.documents.views import document_stream_view


urlpatterns = [
    path(
        "/<uuid:document_uuid>/stream",
        document_stream_view,
        name="api-v1-document-summaries-stream",
    ),
]
