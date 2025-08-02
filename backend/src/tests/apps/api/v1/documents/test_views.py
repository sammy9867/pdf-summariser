import uuid
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse

import pytest

from rest_framework import status
from rest_framework.test import APIClient

from apps.api.v1.documents.serializers import DocumentListSerializer
from apps.documents.factories import DocumentFactory
from apps.documents.models import Document
from apps.documents.services.documents.stream import DocumentSummaryStreamError

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def stream_api_client():
    return Client()


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
        document = Document.objects.get(uuid=result["uuid"])
        assert document.session_key
        assert result == DocumentListSerializer(document).data

    def test_upload__fails_without_file(self, api_client):
        response = api_client.post(self.URL, {}, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["file"] == ["No file was submitted."]


class TestDocumentListView:
    URL = reverse("api-v1-documents-list")

    def test_list__success(self, api_client):
        document = DocumentFactory(session_key=api_client.session.session_key)
        # Different session key, won't be returned
        DocumentFactory()
        response = api_client.get(self.URL, format="json")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result == DocumentListSerializer([document], many=True).data


class TestDocumentSummaryStreamView:
    def _url(self, document=None):
        document_uuid = str(document.uuid) if document else str(uuid.uuid4())
        return reverse(
            "api-v1-document-summaries-stream",
            kwargs={"document_uuid": document_uuid},
        )

    @pytest.fixture
    def document(self, stream_api_client):
        return DocumentFactory(session_key=stream_api_client.session.session_key)

    @patch("apps.api.v1.documents.views.document_stream_summary")
    @patch("apps.api.v1.documents.views.document_can_stream_summary")
    def test_stream__success(
        self,
        mock_can_stream_summary,
        mock_stream_summary,
        stream_api_client,
        document,
    ):
        summary_stream = iter(["Some ", "random ", "text ", "to ", "stream "])
        mock_can_stream_summary.return_value = True
        mock_stream_summary.return_value = summary_stream

        response = stream_api_client.get(self._url(document))
        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"] == "text/event-stream"
        content = b"".join(response.streaming_content).decode("utf-8")

        for summary in summary_stream:
            assert summary in content, content

        mock_can_stream_summary.assert_called_once_with(document)
        mock_stream_summary.assert_called_once_with(document)

    def test_stream__fails_when_document_does_not_exist(self, stream_api_client):
        response = stream_api_client.get(self._url())
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_stream__fails_with_invalid_session(self, document):
        response = Client().get(self._url(document))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch("apps.api.v1.documents.views.document_can_stream_summary")
    def test_stream__fails_while_file_path_is_invalid(
        self,
        mock_can_stream_summary,
        stream_api_client,
        document,
    ):
        error = DocumentSummaryStreamError(
            code=DocumentSummaryStreamError.Code.INVALID_FILE_PATH
        )
        mock_can_stream_summary.side_effect = error

        response = stream_api_client.get(self._url(document))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.content.decode() == error.message
