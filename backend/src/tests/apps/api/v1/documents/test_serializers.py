from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.serializers import DateTimeField

import pytest

from apps.api.v1.documents.serializers import (
    DocumentListSerializer,
    DocumentUploadSerializer,
    UploadedFileSerializer,
)
from apps.documents.factories import DocumentFactory, UploadedFileFactory

pytestmark = pytest.mark.django_db


def test_uploaded_file_serializer():
    uploaded_file = UploadedFileFactory()
    assert {
        "created": DateTimeField().to_representation(uploaded_file.created),
        "modified": DateTimeField().to_representation(uploaded_file.modified),
        "name": uploaded_file.name,
        "size": uploaded_file.size,
        "url": uploaded_file.url,
        "uuid": str(uploaded_file.uuid),
    } == UploadedFileSerializer(uploaded_file).data


def test_document_list_serializer():
    document = DocumentFactory()
    assert {
        "created": DateTimeField().to_representation(document.created),
        "modified": DateTimeField().to_representation(document.modified),
        "uploaded_file": UploadedFileSerializer(document.uploaded_file).data,
        "uuid": str(document.uuid),
    } == DocumentListSerializer(document).data


class TestDocumentUploadSerializer:
    def test_is_valid__success(self):
        file = SimpleUploadedFile("test.txt", b"hello world", content_type="text/plain")
        serializer = DocumentUploadSerializer(data={"file": file})
        assert serializer.is_valid()

    def test_is_valid__fails(self):
        serializer = DocumentUploadSerializer(data={"file": None})
        assert not serializer.is_valid()
