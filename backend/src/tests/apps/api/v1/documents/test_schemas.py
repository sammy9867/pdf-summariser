from datetime import datetime

import pytest

from apps.documents.factories import DocumentFactory, UploadedFileFactory
from apps.api.v1.documents.schemas import (
    UploadedFileSchema,
    DocumentListSchema,
    ErrorSchema,
)

pytestmark = pytest.mark.django_db


def _format_datetime(date_time: datetime):
    return date_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def test_uploaded_file_schema():
    uploaded_file = UploadedFileFactory()
    expected = {
        "created": _format_datetime(uploaded_file.created),
        "modified": _format_datetime(uploaded_file.modified),
        "name": uploaded_file.name,
        "size": uploaded_file.size,
        "uuid": str(uploaded_file.uuid),
    }
    actual = UploadedFileSchema.from_orm(uploaded_file).model_dump(mode="json")
    assert actual == expected


def test_document_list_schema():
    document = DocumentFactory()
    expected = {
        "created": _format_datetime(document.created),
        "modified": _format_datetime(document.modified),
        "uploaded_file": {
            "created": _format_datetime(document.uploaded_file.created),
            "modified": _format_datetime(document.uploaded_file.modified),
            "name": document.uploaded_file.name,
            "size": document.uploaded_file.size,
            "uuid": str(document.uploaded_file.uuid),
        },
        "uuid": str(document.uuid),
    }
    actual = DocumentListSchema.from_orm(document).model_dump(mode="json")
    assert actual == expected


def test_error_schema():
    error = ErrorSchema(detail="Something went wrong")
    expected = {"detail": "Something went wrong"}
    assert error.dict() == expected
