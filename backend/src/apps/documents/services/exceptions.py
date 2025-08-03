from enum import StrEnum


class ServiceError(Exception):
    message: str | None = ""

    class Code(StrEnum):
        pass

    def __init__(self, code: Code):
        if code:
            self.message = f"{self.message}: {code}"

        self.code = code
        super().__init__(self.message)

    def __str__(self):
        return self.message


class DocumentCreateError(ServiceError):
    message = "Document Create error"

    class Code(ServiceError.Code):
        FILE_UPLOAD_FAILED = "File upload failed"


class DocumentSummaryStreamError(ServiceError):
    class Code:
        PDF_PROCESSING_ERROR = "pdf_processing_error"


class UploadedFileCreateError(ServiceError):
    message = "Uploaded File create error"

    class Code(ServiceError.Code):
        FILE_UPLOAD_FAILED = "File upload failed"


class UploadedFileGetContentError(ServiceError):
    message = "Uploaded File get content error"

    class Code(ServiceError.Code):
        FILE_DOWNLOAD_FAILED = "File download failed"
