import logging

from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.documents.models import UploadedFile
from apps.documents.services.exceptions import UploadedFileCreateError
from apps.documents.services.uploaded_files.s3 import s3_upload_file

logger = logging.getLogger(__name__)


def uploaded_file_create(file: InMemoryUploadedFile) -> UploadedFile:
    codes = UploadedFileCreateError.Code
    try:
        s3_key = s3_upload_file(file)
    except Exception as e:
        logger.error(f"Exception while uploading file to S3: {e}")
        raise UploadedFileCreateError(code=codes.FILE_UPLOAD_FAILED)

    uploaded_file = UploadedFile.objects.create(
        s3_key=s3_key,
        name=file.name,
        size=file.size,
        content_type=getattr(file, "content_type", None),
    )
    return uploaded_file
