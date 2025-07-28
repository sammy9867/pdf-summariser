from rest_framework import serializers

from apps.documents.models import Document, UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        read_only_fields = ["file", "name", "size", "created", "modified"]
        fields = read_only_fields

    def get_file(self, obj) -> str | None:
        return obj.file.url if obj.file else None


class DocumentListSerializer(serializers.ModelSerializer):
    uploaded_file = UploadedFileSerializer(read_only=True)

    class Meta:
        model = Document
        read_only_fields = [
            "id",
            "session_id",
            "uploaded_file",
            "uuid",
            "created",
            "modified",
        ]
        fields = read_only_fields


class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data) -> Document:
        request = self.context["request"]
        session_id = request.session.session_key
        if not session_id:
            request.session.save()
            session_id = request.session.session_key

        uploaded_file = UploadedFile.objects.create(
            file=validated_data["file"],
            name=validated_data["file"].name,
            size=validated_data["file"].size,
        )
        document = Document.objects.create(
            session_id=session_id, uploaded_file=uploaded_file
        )

        return document
