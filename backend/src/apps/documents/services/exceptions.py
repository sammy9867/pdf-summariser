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


class DocumentSummaryStreamError(ServiceError):
    message = "Document Summary stream error"

    class Code(ServiceError.Code):
        INVALID_FILE_PATH = "Invalid file path"
