import logging
from typing import AsyncGenerator
from io import BytesIO

import pypdf

from apps.documents.models import Document
from apps.documents.services.exceptions import DocumentSummaryStreamError
from apps.documents.services.uploaded_files.get import uploaded_file_get_content

logger = logging.getLogger(__name__)


async def _extract_text_from_pdf(pdf_content: bytes) -> str:
    codes = DocumentSummaryStreamError.Code
    try:
        pdf_file = BytesIO(pdf_content)
        pdf_reader = pypdf.PdfReader(pdf_file)

        text_content = ""
        # Read first few pages (limit to avoid too much content)
        max_pages = min(3, len(pdf_reader.pages))

        for page_num in range(max_pages):
            page = pdf_reader.pages[page_num]
            text_content += page.extract_text() + "\n"

        return text_content.strip()
    except Exception as e:
        logger.error(f"Exception while extracting text from PDF: {e}")
        raise DocumentSummaryStreamError(codes.PDF_PROCESSING_ERROR)


async def document_stream_summary(document: Document) -> AsyncGenerator:
    file_content = await uploaded_file_get_content(document.uploaded_file)
    text_content = await _extract_text_from_pdf(file_content)

    if not text_content:
        yield "No readable content found in the document."
        return

    words = text_content.split()
    max_words = min(500, len(words))
    limited_content = " ".join(words[:max_words])

    for word in limited_content.split():
        yield f"{word} "
