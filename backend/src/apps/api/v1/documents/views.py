import json

from django.http import HttpRequest, StreamingHttpResponse

from ninja import File, Router
from ninja.files import UploadedFile as NinjaUploadedFile

from apps.api.v1.documents.schemas import DocumentListSchema, ErrorSchema
from apps.documents.models import Document
from apps.documents.services.documents.create import document_create
from apps.documents.services.documents.stream import document_stream_summary

router = Router()


@router.post(
    "upload",
    response={201: DocumentListSchema},
    url_name="documents-upload",
)
async def document_upload_view(
    request: HttpRequest, file: NinjaUploadedFile = File(...)
):
    session_key = request.session.session_key
    return await document_create(file, session_key)


@router.get(
    "",
    response=list[DocumentListSchema],
    url_name="documents-list",
)
async def document_list_view(request: HttpRequest):
    session_key = request.session.session_key
    if not session_key:
        return []

    queryset = (
        Document.objects.filter(session_key=session_key)
        .select_related("uploaded_file")
        .order_by("-created")
    )
    return [document async for document in queryset]


@router.get(
    "{document_uuid}/stream",
    response={404: ErrorSchema},
    url_name="documents-stream",
)
async def document_stream_view(request: HttpRequest, document_uuid: str):
    document = (
        await Document.objects.filter(
            uuid=document_uuid,
            session_key=request.session.session_key,
        )
        .select_related("uploaded_file")
        .afirst()
    )
    if not document:
        return 404, {"detail": "Document not found"}

    async def generate_sse_event_stream():
        async for word in document_stream_summary(document):
            data = {"type": "summary", "summary": word}
            yield f"data: {json.dumps(data)}\n\n"

        end_data = {"type": "end"}
        yield f"data: {json.dumps(end_data)}\n\n"

    response = StreamingHttpResponse(
        generate_sse_event_stream(),
        content_type="text/event-stream",
    )
    response["Cache-Control"] = "no-cache"
    return response
