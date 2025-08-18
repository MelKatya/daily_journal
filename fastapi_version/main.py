from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

import uvicorn
from api import router as api_router
from core.config import settings
from core.models import db_helper
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa B008
    """
    Контекстный менеджер жизненного цикла приложения.
    При завершении работы приложения освобождает ресурсы подключения к БД.
    """
    yield
    await db_helper.dispose()


base_dir: Path = Path(__file__).resolve().parent
templates = settings.templates

main_app = FastAPI(lifespan=lifespan)
main_app.include_router(api_router)
main_app.mount(
    "/static",
    StaticFiles(directory=base_dir / "static"),
    name="static",
)


@main_app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> Response:
    """
    Обработчик исключений StarletteHTTPException.

    Если в заголовках присутствует ключ 'Location', выполняет редирект.
    В противном случае возвращает HTML-страницу с кодом ошибки и сообщением.
    """
    if exc.headers is not None and "Location" in exc.headers:
        return RedirectResponse(
            exc.headers["Location"],
            status_code=exc.status_code,
        )

    return templates.TemplateResponse(
        name="mistakes.html",
        context={
            "request": request,
            "code": exc.status_code,
            "message": str(exc.detail),
        },
    )


@main_app.get("/", response_class=HTMLResponse)
def home_page() -> RedirectResponse:
    """
    Корневой маршрут.
    Возвращает редирект на страницу авторизации ('/login').
    """
    return RedirectResponse("/login")


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
