from ninja import NinjaAPI
from ninja.errors import ValidationError

from apps.api.v1.api import router as api_v1_router

ninja_api = NinjaAPI(
    title="PDF Summariser API",
    description="API for PDF document summarisation",
    version="v1",
)
ninja_api.add_router("v1/", api_v1_router)


@ninja_api.exception_handler(ValidationError)
def validation_error(request, exc):
    # Default validation error return 422 status code
    return ninja_api.create_response(request, {"detail": exc.errors}, status=400)
