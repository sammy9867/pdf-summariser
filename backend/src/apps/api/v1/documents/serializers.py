from rest_framework import serializers

from apps.documents.models import Document, UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ["file", "name", "size", "created", "modified"]
        read_only_fields = ["created", "modified"]


class DocumentListSerializer(serializers.ModelSerializer):
    uploaded_file = UploadedFileSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ["id", "session_id", "uploaded_file", "uuid", "created", "modified"]
        read_only_fields = [
            "id",
            "session_id",
            "uploaded_file",
            "uuid",
            "created",
            "modified",
        ]


class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
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
