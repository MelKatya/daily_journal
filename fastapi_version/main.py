from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.config import settings
from api import router as api_router
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


base_dir: Path = Path(__file__).resolve().parent
templates = settings.templates

main_app = FastAPI(lifespan=lifespan)
main_app.include_router(api_router)
main_app.mount("/static", StaticFiles(directory=base_dir / "static"), name="static",)


@main_app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if "Location" in exc.headers:
        return RedirectResponse(exc.headers["Location"], status_code=exc.status_code)

    template_response = templates.TemplateResponse(
        name="mistakes.html",
        context={
            "request": request,
            "code": exc.status_code,
            "message": str(exc.detail)
        }
    )
    return template_response


@main_app.get("/", response_class=HTMLResponse)
def home_page():
    """
    Корневой маршрут: перенаправляет на страницу входа пользователя.
    """
    return RedirectResponse("/login")


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
