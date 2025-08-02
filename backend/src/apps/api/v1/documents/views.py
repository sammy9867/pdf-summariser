import json

from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.api.v1.documents.serializers import (
    DocumentListSerializer,
    DocumentUploadSerializer,
)
from apps.api.v1.documents.utils import get_session_key_from_request
from apps.documents.models import Document
from apps.documents.services.documents.stream import document_stream_summary


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


class DocumentListView(ListAPIView):
    pagination_class = None
    permission_classes = [AllowAny]
    serializer_class = DocumentListSerializer

    def get_queryset(self):
        session_key = get_session_key_from_request(self.request)
        if not session_key:
            return Document.objects.none()
        return Document.objects.filter(session_key=session_key).order_by("-created")


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
