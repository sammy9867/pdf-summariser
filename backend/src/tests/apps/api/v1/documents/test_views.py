import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from apps.api.v1.documents.serializers import DocumentListSerializer
from apps.documents.factories import DocumentFactory
from apps.documents.models import Document

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


class TestDocumentUploadView:
    URL = reverse("api-v1-documents-upload")

    @pytest.fixture
    def file(self):
        return SimpleUploadedFile("test.txt", b"hello world", content_type="text/plain")

    @pytest.fixture
    def payload(self, file):
        return {"file": file}

    def test_upload__success(self, api_client, payload):
        response = api_client.post(self.URL, payload, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        result = response.json()
        document = Document.objects.get(id=result["id"])
        assert document.session_id
        assert result == DocumentListSerializer(document).data

    def test_upload__fails_without_file(self, api_client):
        response = api_client.post(self.URL, {}, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["file"] == ["No file was submitted."]


class TestDocumentListView:
    URL = reverse("api-v1-documents-list")

    def test_list__success(self, api_client):
        document = DocumentFactory(session_id=api_client.session.session_key)
        # Different session key, won't be returned
        DocumentFactory()
        response = api_client.get(self.URL, format="json")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result == DocumentListSerializer([document], many=True).data
