from ninja import NinjaAPI

from apps.api.v1.api import router as api_v1_router

ninja_api = NinjaAPI(
    title="PDF Summariser API", description="API for PDF document summarisation"
)
ninja_api.add_router("v1/", api_v1_router)
