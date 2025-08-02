from unittest.mock import patch

import pytest

from apps.documents.factories import DocumentFactory
from apps.documents.services.documents.stream import document_stream_summary

pytestmark = pytest.mark.django_db


class TestDocumentStreamSummary:
    @pytest.fixture
    def document(self):
        return DocumentFactory()

    @patch("time.sleep")
    def test_stream__success(self, document):
        summary = document_stream_summary(document)
        results = list(summary)
        combined_text = "".join(results)
        assert "Some random text to stream" in combined_text
