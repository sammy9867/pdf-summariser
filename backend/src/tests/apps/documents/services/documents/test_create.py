from unittest.mock import patch


from django.core.files.uploadedfile import SimpleUploadedFile

import pytest

from apps.documents.models import Document
from apps.documents.services.documents.create import (
    DocumentCreateError,
    document_create,
)

pytestmark = pytest.mark.django_db


class TestDocumentCreate:
    @pytest.fixture
    def file(self):
        return SimpleUploadedFile("test.txt", b"hello world", content_type="text/plain")

    @patch("apps.documents.services.uploaded_files.create.s3_upload_file")
    def test_create__success(self, mock_s3_upload_file, file):
        mock_s3_upload_file.return_value = "s3_key"
        document = document_create(file, session_key="session_key")
        assert document.session_key == "session_key"
        uploaded_file = document.uploaded_file
        assert uploaded_file.s3_key == "s3_key"
        assert uploaded_file.name == file.name
        assert uploaded_file.size == file.size
        assert uploaded_file.content_type == file.content_type

    @patch("apps.documents.services.uploaded_files.create.s3_upload_file")
    def test_create__fails_when_uploading_file(self, mock_s3_upload_file, file):
        mock_s3_upload_file.side_effect = Exception("exception")
        with pytest.raises(DocumentCreateError):
            document_create(file, session_key="session_key")

        assert not Document.objects.exists()
