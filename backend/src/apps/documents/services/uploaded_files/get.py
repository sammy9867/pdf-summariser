import logging

from apps.documents.models import UploadedFile
from apps.documents.services.exceptions import UploadedFileGetContentError
from apps.documents.services.uploaded_files.s3 import s3_download_file

logger = logging.getLogger(__name__)


def uploaded_file_get_content(uploaded_file: UploadedFile) -> bytes:
    codes = UploadedFileGetContentError.Code
    try:
        return s3_download_file(uploaded_file.s3_key)
    except Exception as e:
        logger.error(f"Exception while downloading file from S3: {e}")
        raise UploadedFileGetContentError(code=codes.FILE_DOWNLOAD_FAILED)
