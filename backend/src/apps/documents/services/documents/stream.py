import time
from typing import Generator

from apps.documents.models import Document


def document_stream_summary(document: Document) -> Generator[str, None, None]:
    # Mock stream for now
    summary = "Some random text to stream"
    for word in summary.split(" "):
        yield f"{word} "
        time.sleep(0.03)
