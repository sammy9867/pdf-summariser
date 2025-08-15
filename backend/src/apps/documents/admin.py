from django.contrib import admin
from apps.documents.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["uuid", "session_key", "created"]
    readonly_fields = [
        "uuid",
        "session_key",
        "created",
        "modified",
        "file_name",
        "file_size",
        "file_content_type",
    ]
    fields = readonly_fields

    def file_name(self, obj: Document) -> str:
        return obj.uploaded_file.name

    def file_size(self, obj: Document) -> int:
        return obj.uploaded_file.size

    def file_content_type(self, obj: Document) -> str | None:
        return obj.uploaded_file.content_type
