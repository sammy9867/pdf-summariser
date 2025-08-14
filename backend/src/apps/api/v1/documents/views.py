import json

from django.http import HttpRequest, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ninja import Router

from apps.api.v1.documents.schema import DocumentListSchema
from apps.api.v1.documents.serializers import (
    DocumentListSerializer,
    DocumentUploadSerializer,
)
from apps.api.v1.documents.utils import get_session_key_from_request
from apps.documents.models import Document
from apps.documents.services.documents.stream import document_stream_summary

router = Router()


class DocumentUploadView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = DocumentUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        return Response(
            DocumentListSerializer(document).data, status=status.HTTP_201_CREATED
        )


@router.get("", response=list[DocumentListSchema])
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


@csrf_exempt
@require_GET
def document_stream_view(request, document_uuid):
    session_key = get_session_key_from_request(request)
    document = get_object_or_404(Document, uuid=document_uuid, session_key=session_key)

    def generate_sse_event_stream():
        for word in document_stream_summary(document):
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
