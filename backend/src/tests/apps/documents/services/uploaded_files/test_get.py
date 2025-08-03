from unittest.mock import patch

import pytest

from apps.documents.factories import UploadedFileFactory
from apps.documents.services.exceptions import UploadedFileGetContentError
from apps.documents.services.uploaded_files.get import uploaded_file_get_content

pytestmark = pytest.mark.django_db


class TestUploadedFileGetContent:
    @pytest.fixture
    def uploaded_file(self):
        return UploadedFileFactory()

    @patch("apps.documents.services.uploaded_files.get.s3_download_file")
    def test_get__success(self, mock_s3_download_file, uploaded_file):
        mock_s3_download_file.return_value = b"PDF summary"
        content = uploaded_file_get_content(uploaded_file)
        assert content == b"PDF summary"

    @patch("apps.documents.services.uploaded_files.get.s3_download_file")
    def test_get__fails_when_downloading_file(
        self, mock_s3_download_file, uploaded_file
    ):
        mock_s3_download_file.side_effect = Exception("exception")
        with pytest.raises(UploadedFileGetContentError):
            uploaded_file_get_content(uploaded_file)
