from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.config import settings
from api import router as api_router
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(api_router)
main_app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
