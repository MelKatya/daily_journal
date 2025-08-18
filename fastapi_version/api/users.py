from fastapi import APIRouter, Cookie, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils import check_auth
from core.config import settings
from core.models import User, db_helper
from core.schemas.users import LoginForm, RegistrationForm, UserCreate
from crud.user import check_name_exists, create_user
from security.utils import create_jwt_token, get_password_hash, verify_password

router = APIRouter(tags=["Users"])
templates = settings.templates


@router.get("/registration", response_class=HTMLResponse)
async def show_registration_form(request: Request) -> HTMLResponse:
    """
    Обрабатывает GET-запрос с формой регистрации.

    Args:
        request (Request): объект запроса FastAPI.
    """
    form = RegistrationForm()
    return templates.TemplateResponse(
        name="register.html", context={"request": request, "form": form}
    )


@router.post("/registration", response_class=HTMLResponse)
async def process_registration(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa B008
) -> HTMLResponse | RedirectResponse:
    """
    Обрабатывает POST-запрос формы регистрации нового пользователя.
    - Проверяет валидность введенных данных.
    - Создает нового пользователя с помощью 'create_user'.
    - Перенаправляет на страницу авторизации.

    Args:
        request (Request): объект запроса FastAPI.
        session (AsyncSession): асинхронная сессия SQLAlchemy.

    Returns:
        HTMLResponse | RedirectResponse: редирект на страницу /login при
            успешной регистрации или страницу регистрации с ошибками формы.
    """
    form_data = await request.form()
    form = RegistrationForm(form_data)

    if form.validate():
        name, email, password = (
            str(form.name.data),
            str(form.email.data),
            str(form.password.data),
        )
        hashed_password = get_password_hash(password)
        new_user = UserCreate(
            name=name,
            email=email,
            hashed_password=hashed_password,
        )
        await create_user(session, new_user)

        return RedirectResponse("/login", status_code=303)

    else:
        return templates.TemplateResponse(
            "register.html", {"request": request, "form": form}
        )


@router.get("/login", response_class=HTMLResponse)
async def show_login_form(
    request: Request,
    token: str | None = Cookie(default=None),  # noqa B008
) -> HTMLResponse | RedirectResponse:
    """
    Обрабатывает GET-запрос формы авторизации.
    Если токен найден в cookies, перенаправляет пользователя на домашнюю
        страницу.
    Если токена нет, возвращает страницу с формой авторизации.

    Args:
        request (Request): объект запроса FastAPI.
        token (str | None): JWT-токен из cookies, если он существует.

    Returns:
        HTMLResponse | RedirectResponse:
            - RedirectResponse — редирект на /users/home при наличии токена.
            - HTMLResponse — страница авторизации без токена.
    """
    if token:
        return RedirectResponse("/users/home")

    form = LoginForm()
    return templates.TemplateResponse(
        name="login.html", context={"request": request, "form": form}
    )


@router.post("/login", response_class=HTMLResponse)
async def process_login(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa B008
) -> HTMLResponse | RedirectResponse:
    """
    Обрабатывает POST-запрос авторизации пользователя.
    - Проверяет валидность введенных данных.
    - В случае успеха создаёт JWT-токен, сохраняет его в cookies
        и перенаправляет на домашнюю страницу.
    - Перенаправляет на основную страницу пользователя.
    - Если введен неверно логин и/или пароль, то перенаправляет на страницу
        с ошибкой.

    Args:
        request (Request): объект запроса FastAPI.
        session (AsyncSession): асинхронная сессия SQLAlchemy.

    Returns:
        HTMLResponse | RedirectResponse:
            - RedirectResponse — успешная авторизация (переход на /users/home).
            - HTMLResponse — форма авторизации с ошибкой.
    """
    auth_exception = HTTPException(
        status_code=401,
        detail="invalid username or password",
    )

    form_data = await request.form()
    form = LoginForm(form_data)

    if form.validate():
        name, password = str(form.name.data), str(form.password.data)

        if not (user := await check_name_exists(session, name)):
            raise auth_exception

        if not verify_password(password, user.hashed_password):
            raise auth_exception

        token = create_jwt_token(user.id)

        response = RedirectResponse("/users/home", status_code=303)
        response.set_cookie(key="token", value=token, httponly=True)

        return response


@router.get("/logout", response_class=HTMLResponse)
async def logout_user(
    user: User = Depends(check_auth),  # noqa B008
) -> RedirectResponse:
    """
    Выполняет выход пользователя из системы.
    - Удаляет cookie с JWT-токеном.
    - Перенаправляет на страницу авторизации.

    Args:
        user (User): объект текущего пользователя.

    Returns:
        RedirectResponse: редирект на страницу авторизации.
    """
    response = RedirectResponse("/login")
    response.delete_cookie(key="token", httponly=True)
    return response


@router.get("/users/home", response_class=HTMLResponse)
async def user_page(
    request: Request,
    user: User = Depends(check_auth),  # noqa B008
) -> HTMLResponse:
    """
    Отображает личную страницу пользователя (home page).

    Args:
        request (Request): объект запроса FastAPI.
        user (User): объект текущего пользователя.

    Returns:
        HTMLResponse: HTML-страница пользователя.
    """
    return templates.TemplateResponse(
        name="user_page.html", context={"request": request, "name": user.name}
    )
