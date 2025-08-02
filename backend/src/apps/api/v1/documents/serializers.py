from rest_framework import serializers

from apps.api.v1.documents.utils import get_session_key_from_request
from apps.documents.models import Document, UploadedFile
from apps.documents.services.documents.create import document_create


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        read_only_fields = [
            "created",
            "modified",
            "name",
            "size",
            "uuid",
        ]
        fields = read_only_fields


class DocumentListSerializer(serializers.ModelSerializer):
    uploaded_file = UploadedFileSerializer(read_only=True)

    class Meta:
        model = Document
        read_only_fields = [
            "created",
            "modified",
            "uploaded_file",
            "uuid",
        ]
        fields = read_only_fields


class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data) -> Document:
        request = self.context["request"]
        session_key = get_session_key_from_request(request)
        return document_create(validated_data["file"], session_key)
