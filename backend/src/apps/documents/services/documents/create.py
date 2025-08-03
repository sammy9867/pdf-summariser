from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction

from apps.documents.models import Document
from apps.documents.services.exceptions import (
    DocumentCreateError,
    UploadedFileCreateError,
)
from apps.documents.services.uploaded_files.create import uploaded_file_create


@transaction.atomic
def document_create(file: InMemoryUploadedFile, session_key: str) -> Document:
    codes = DocumentCreateError.Code
    try:
        uploaded_file = uploaded_file_create(file)
    except UploadedFileCreateError:
        raise DocumentCreateError(code=codes.FILE_UPLOAD_FAILED)

    return Document.objects.create(session_key=session_key, uploaded_file=uploaded_file)
