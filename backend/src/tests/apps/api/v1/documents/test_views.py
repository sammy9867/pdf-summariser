import uuid
from unittest.mock import patch

from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import AsyncClient
from django.urls import reverse_lazy

import pytest

from apps.api.v1.documents.schemas import DocumentListSchema
from apps.documents.models import Document
from tests.apps.api.v1.documents.utils import (
    create_document,
    dump_with_django_encoder,
)

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def session() -> SessionStore:
    return SessionStore(session_key=str(uuid.uuid4()))


@pytest.fixture
def api_client(session) -> AsyncClient:
    api_client = AsyncClient()
    api_client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key
    return api_client


class TestDocumentUploadView:
    URL = reverse_lazy("api-v1:documents-upload")

    @pytest.fixture
    def file(self):
        return SimpleUploadedFile("test.txt", b"hello world", content_type="text/plain")

    @pytest.fixture
    def payload(self, file):
        return {"file": file}

    @patch("apps.documents.services.uploaded_files.create.s3_upload_file")
    async def test_upload__success(self, mock_s3_upload_file, api_client, payload):
        mock_s3_upload_file.return_value = "s3_key"
        response = await api_client.post(self.URL, payload)
        assert response.status_code == 201
        result = response.json()
        document = await Document.objects.select_related(
            "uploaded_file",
        ).aget(uuid=result["uuid"])
        assert document.session_key
        assert result == dump_with_django_encoder(DocumentListSchema, document)

    async def test_upload__fails_without_file(self, api_client):
        response = await api_client.post(self.URL, {})
        assert response.status_code == 400
        assert response.json()["detail"][0] == {
            "type": "missing",
            "loc": ["file", "file"],
            "msg": "Field required",
        }


class TestDocumentListView:
    URL = reverse_lazy("api-v1:documents-list")

    async def test_list__success(self, api_client, session):
        document = await create_document(session_key=session.session_key)
        # Different session key, won't be returned
        await create_document(session_key=str(uuid.uuid4()))
        response = await api_client.get(self.URL)
        assert response.status_code == 200
        result = response.json()
        assert result == [dump_with_django_encoder(DocumentListSchema, document)]


class TestDocumentSummaryStreamView:
    def _url(self, document=None):
        document_uuid = str(document.uuid) if document else str(uuid.uuid4())
        return reverse_lazy(
            "api-v1:documents-stream",
            kwargs={"document_uuid": document_uuid},
        )

    @patch("apps.api.v1.documents.views.document_stream_summary")
    async def test_stream__success(
        self,
        mock_stream_summary,
        api_client,
        session,
    ):
        async def async_summary_gen(summary_list):
            for summary in summary_list:
                yield summary

        summary_stream = async_summary_gen(
            ["Some ", "random ", "text ", "to ", "stream "]
        )
        mock_stream_summary.return_value = summary_stream
        document = await create_document(session_key=session.session_key)

        response = await api_client.get(self._url(document))
        assert response.status_code == 200
        assert response["Content-Type"] == "text/event-stream"

        content = [data.decode("utf-8") async for data in response.streaming_content]
        async for summary in summary_stream:
            assert summary in content, content

        mock_stream_summary.assert_called_once_with(document)

    async def test_stream__fails_when_document_does_not_exist(self, api_client):
        response = await api_client.get(self._url())
        assert response.status_code == 404
        assert response.json()["detail"] == "Document not found"

    async def test_stream__fails_with_invalid_session(self, session):
        document = await create_document(session_key=session.session_key)
        response = await AsyncClient().get(self._url(document))
        assert response.status_code == 404
        assert response.json()["detail"] == "Document not found"
