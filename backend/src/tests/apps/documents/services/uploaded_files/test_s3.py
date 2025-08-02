from unittest.mock import Mock, patch

from botocore.exceptions import ClientError

from django.core.files.uploadedfile import SimpleUploadedFile

import pytest

from apps.documents.services.uploaded_files.s3 import s3_upload_file

pytestmark = pytest.mark.django_db


class TestS3UploadFile:
    @pytest.fixture
    def file(self):
        return SimpleUploadedFile("test.txt", b"hello world", content_type="text/plain")

    @patch("apps.documents.services.uploaded_files.s3._ensure_bucket_exists")
    @patch("apps.documents.services.uploaded_files.s3._get_client")
    def test_upload__success(self, mock_get_client, mock_ensure_bucket_exists, file):
        mock_get_client.return_value = Mock()
        mock_ensure_bucket_exists.return_value = True
        assert s3_upload_file(file)

    @patch("apps.documents.services.uploaded_files.s3._ensure_bucket_exists")
    @patch("apps.documents.services.uploaded_files.s3._get_client")
    def test_upload__fails_if_bucket_does_not_exist(
        self, mock_get_client, mock_ensure_bucket_exists, file
    ):
        mock_get_client.return_value = Mock()
        mock_ensure_bucket_exists.side_effect = ClientError(
            error_response={},
            operation_name="some operation name",
        )
        with pytest.raises(ClientError):
            s3_upload_file(file)

    @patch("apps.documents.services.uploaded_files.s3._ensure_bucket_exists")
    @patch("apps.documents.services.uploaded_files.s3._get_client", autospec=True)
    def test_upload__fails_on_file_upload(
        self, mock_get_client, mock_ensure_bucket_exists, file
    ):
        mock = Mock()
        mock_get_client.return_value = mock
        mock.upload_fileobj.side_effect = ClientError(
            error_response={},
            operation_name="some operation name",
        )
        mock_ensure_bucket_exists.return_value = True
        with pytest.raises(ClientError):
            s3_upload_file(file)
