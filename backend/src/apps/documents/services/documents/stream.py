import os
import time
from typing import Generator

from apps.documents.models import Document
from apps.documents.services.exceptions import DocumentSummaryStreamError


def document_can_stream_summary(
    document: Document, raise_exception: bool = True
) -> bool:
    codes = DocumentSummaryStreamError.Code
    try:
        file_path = document.uploaded_file.file.path

        if not os.path.exists(file_path):
            raise DocumentSummaryStreamError(codes.INVALID_FILE_PATH)
    except DocumentSummaryStreamError as e:
        if raise_exception:
            raise e
        return False
    return True


def document_stream_summary(document: Document) -> Generator[str, None, None]:
    # Mock stream for now
    summary = "Some random text to stream"
    for word in summary.split(" "):
        yield f"{word} "
        time.sleep(0.03)
