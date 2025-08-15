from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile

import pytest

from botocore.exceptions import ClientError

from apps.documents.models import UploadedFile
from apps.documents.services.exceptions import UploadedFileCreateError
from apps.documents.services.uploaded_files.create import uploaded_file_create

pytestmark = pytest.mark.django_db(transaction=True)


class TestUploadedFileCreate:
    @pytest.fixture
    def file(self):
        return SimpleUploadedFile("test.txt", b"hello world", content_type="text/plain")

    @patch("apps.documents.services.uploaded_files.create.s3_upload_file")
    async def test_create__success(self, mock_s3_upload_file, file):
        mock_s3_upload_file.return_value = "s3_key"
        uploaded_file = await uploaded_file_create(file)
        assert uploaded_file.s3_key == "s3_key"
        assert uploaded_file.name == file.name
        assert uploaded_file.size == file.size
        assert uploaded_file.content_type == file.content_type

    @patch("apps.documents.services.uploaded_files.create.s3_upload_file")
    async def test_create__fails_when_uploading_file(self, mock_s3_upload_file, file):
        mock_s3_upload_file.side_effect = ClientError(
            error_response={},
            operation_name="some operation name",
        )
        with pytest.raises(UploadedFileCreateError):
            await uploaded_file_create(file)

        assert not await UploadedFile.objects.aexists()
