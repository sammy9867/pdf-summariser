from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from apps.api.v1.documents.serializers import (
    DocumentListSerializer,
    DocumentUploadSerializer,
)
from apps.documents.models import Document


class DocumentUploadView(CreateAPIView):
    serializer_class = DocumentUploadSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        return Response(
            DocumentListSerializer(document).data, status=status.HTTP_201_CREATED
        )


class DocumentListView(ListAPIView):
    serializer_class = DocumentListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        session_id = self.request.session.session_key
        if not session_id:
            return Document.objects.none()
        return Document.objects.filter(session_id=session_id).order_by("-created")
