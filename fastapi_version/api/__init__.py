from fastapi import APIRouter

from .users import router as users_router
from .tasks import router as tasks_router

router = APIRouter()
router.include_router(users_router)
router.include_router(tasks_router)
