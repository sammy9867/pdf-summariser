from unittest.mock import patch

import pytest

from apps.documents.factories import DocumentFactory
from apps.documents.services.exceptions import DocumentSummaryStreamError
from apps.documents.services.documents.stream import document_stream_summary

pytestmark = pytest.mark.django_db


class TestDocumentStreamSummary:
    @pytest.fixture
    def document(self):
        return DocumentFactory()

    @patch("apps.documents.services.documents.stream._extract_text_from_pdf")
    @patch("apps.documents.services.uploaded_files.get.s3_download_file")
    def test_stream__success(
        self, mock_s3_download_file, mock_extract_text_from_pdf, document
    ):
        mock_s3_download_file.return_value = b"PDF summary"
        mock_extract_text_from_pdf.return_value = "PDF summary"
        summary = document_stream_summary(document)
        results = list(summary)
        combined_text = "".join(results)
        assert "PDF summary" in combined_text

    @patch("apps.documents.services.documents.stream._extract_text_from_pdf")
    @patch("apps.documents.services.uploaded_files.get.s3_download_file")
    def test_stream__fails(
        self, mock_s3_download_file, mock_extract_text_from_pdf, document
    ):
        mock_s3_download_file.return_value = b"PDF summary"
        mock_extract_text_from_pdf.side_effect = DocumentSummaryStreamError(
            code=DocumentSummaryStreamError.Code.PDF_PROCESSING_ERROR,
        )
        with pytest.raises(DocumentSummaryStreamError):
            list(document_stream_summary(document))
