from ninja import Router

from apps.api.v1.documents.views import router as documents_router

router = Router()
router.add_router("documents", documents_router)
