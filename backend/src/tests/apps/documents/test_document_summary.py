from unittest.mock import Mock, patch

import pytest

from apps.documents.factories import DocumentFactory
from apps.documents.services.document_summary import (
    DocumentSummaryStreamError,
    document_can_stream_summary,
    document_stream_summary,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def document():
    return DocumentFactory()


class TestDocumentCanStreamSummary:
    @patch("os.path.exists", new=Mock(return_value=True))
    def test__can_stream__success(self, document):
        assert document_can_stream_summary(document)

    @patch("os.path.exists", new=Mock(return_value=False))
    def test__can_stream__fails(self, document):
        with pytest.raises(DocumentSummaryStreamError) as exc_info:
            document_can_stream_summary(document)

        assert exc_info.value.code == DocumentSummaryStreamError.Code.INVALID_FILE_PATH


class TestDocumentStreamSummary:
    @patch("time.sleep")
    def test__stream__success(self, document):
        summary = document_stream_summary(document)
        results = list(summary)
        combined_text = "".join(results)
        assert "Some random text to stream" in combined_text
