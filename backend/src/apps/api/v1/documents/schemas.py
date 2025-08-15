from ninja import ModelSchema, Schema

from apps.documents.models import Document, UploadedFile


class UploadedFileSchema(ModelSchema):
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


class DocumentListSchema(ModelSchema):
    uploaded_file: UploadedFileSchema

    class Meta:
        model = Document
        read_only_fields = [
            "created",
            "modified",
            "uploaded_file",
            "uuid",
        ]
        fields = read_only_fields


class ErrorSchema(Schema):
    detail: str
