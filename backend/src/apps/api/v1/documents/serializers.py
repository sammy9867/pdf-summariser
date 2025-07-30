from rest_framework import serializers

from apps.api.v1.documents.utils import get_session_id_from_request
from apps.documents.models import Document, UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        read_only_fields = ["created", "file", "modified", "name", "size"]
        fields = read_only_fields

    def get_file(self, obj) -> str | None:
        return obj.file.url if obj.file else None


class DocumentListSerializer(serializers.ModelSerializer):
    uploaded_file = UploadedFileSerializer(read_only=True)

    class Meta:
        model = Document
        read_only_fields = [
            "created",
            "modified",
            "session_id",
            "uploaded_file",
            "uuid",
        ]
        fields = read_only_fields


class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data) -> Document:
        request = self.context["request"]
        session_id = get_session_id_from_request(request)

        uploaded_file = UploadedFile.objects.create(
            file=validated_data["file"],
            name=validated_data["file"].name,
            size=validated_data["file"].size,
        )
        document = Document.objects.create(
            session_id=session_id, uploaded_file=uploaded_file
        )

        return document
