from django.urls import include, path

from apps.api.v1.documents import urls as document_urls


urlpatterns = [
    path("documents", include(document_urls)),
]
