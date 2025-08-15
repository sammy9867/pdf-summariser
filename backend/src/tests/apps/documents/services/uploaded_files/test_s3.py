from unittest.mock import AsyncMock, patch

from botocore.exceptions import ClientError

from django.core.files.uploadedfile import SimpleUploadedFile

import pytest

from apps.documents.services.uploaded_files.s3 import s3_download_file, s3_upload_file

pytestmark = pytest.mark.django_db(transaction=True)


class TestS3UploadFile:
    @pytest.fixture
    def file(self):
        return SimpleUploadedFile("test.txt", b"hello world", content_type="text/plain")

    @patch("apps.documents.services.uploaded_files.s3._ensure_bucket_exists")
    @patch("apps.documents.services.uploaded_files.s3._get_client")
    async def test_upload__success(
        self, mock_get_client, mock_ensure_bucket_exists, file
    ):
        mock = AsyncMock()
        mock.__aenter__.return_value = AsyncMock()
        mock_get_client.return_value = mock
        mock_ensure_bucket_exists.return_value = AsyncMock()

        assert await s3_upload_file(file)

    @patch("apps.documents.services.uploaded_files.s3._ensure_bucket_exists")
    @patch("apps.documents.services.uploaded_files.s3._get_client")
    async def test_upload__fails_if_bucket_does_not_exist(
        self, mock_get_client, mock_ensure_bucket_exists, file
    ):
        mock = AsyncMock()
        mock.__aenter__.return_value = AsyncMock()
        mock_get_client.return_value = mock
        mock_ensure_bucket_exists.side_effect = ClientError(
            error_response={},
            operation_name="some operation name",
        )
        with pytest.raises(ClientError):
            await s3_upload_file(file)

    @patch("apps.documents.services.uploaded_files.s3._ensure_bucket_exists")
    @patch("apps.documents.services.uploaded_files.s3._get_client", autospec=True)
    async def test_upload__fails_on_file_upload(
        self, mock_get_client, mock_ensure_bucket_exists, file
    ):
        s3_client = AsyncMock()
        s3_client.upload_fileobj.side_effect = ClientError(
            error_response={},
            operation_name="some operation name",
        )
        mock = AsyncMock()
        mock.__aenter__.return_value = s3_client
        mock_get_client.return_value = mock
        mock_ensure_bucket_exists.return_value = AsyncMock()

        with pytest.raises(ClientError):
            await s3_upload_file(file)


class TestS3DownloadFile:
    @patch("apps.documents.services.uploaded_files.s3._ensure_bucket_exists")
    @patch("apps.documents.services.uploaded_files.s3._get_client", autospec=True)
    async def test_download__success(self, mock_get_client, mock_ensure_bucket_exists):
        s3_client = AsyncMock()
        s3_client.get_object.return_value = AsyncMock({"Body": "erer"})
        mock = AsyncMock()
        mock.__aenter__.return_value = s3_client
        mock_get_client.return_value = mock
        mock_ensure_bucket_exists.return_value = AsyncMock()

        assert await s3_download_file("s3_key")

    @patch("apps.documents.services.uploaded_files.s3._ensure_bucket_exists")
    @patch("apps.documents.services.uploaded_files.s3._get_client")
    async def test_download_fails_if_bucket_does_not_exist(
        self, mock_get_client, mock_ensure_bucket_exists
    ):
        mock = AsyncMock()
        mock.__aenter__.return_value = AsyncMock()
        mock_get_client.return_value = mock
        mock_ensure_bucket_exists.side_effect = ClientError(
            error_response={},
            operation_name="some operation name",
        )
        with pytest.raises(ClientError):
            await s3_download_file("s3_key")

    @patch("apps.documents.services.uploaded_files.s3._ensure_bucket_exists")
    @patch("apps.documents.services.uploaded_files.s3._get_client", autospec=True)
    async def test_download__fails_on_file_download(
        self, mock_get_client, mock_ensure_bucket_exists
    ):
        s3_client = AsyncMock()
        s3_client.get_object.side_effect = ClientError(
            error_response={},
            operation_name="some operation name",
        )
        mock = AsyncMock()
        mock.__aenter__.return_value = s3_client
        mock_get_client.return_value = mock
        mock_ensure_bucket_exists.return_value = AsyncMock()

        with pytest.raises(ClientError):
            await s3_download_file("s3_key")
