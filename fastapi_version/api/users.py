from fastapi import APIRouter, Cookie, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils import check_auth
from core.config import settings
from core.models import db_helper
from core.schemas.users import LoginForm, RegistrationForm, UserCreate
from crud.user import check_name_exists, create_user
from security.utils import create_jwt_token, get_password_hash, verify_password

router = APIRouter(tags=["Users"])
templates = settings.templates


@router.get("/registration", response_class=HTMLResponse)
async def show_registration_form(request: Request):
    form = RegistrationForm()
    return templates.TemplateResponse(
        name="register.html", context={"request": request, "form": form}
    )


@router.post("/registration", response_class=HTMLResponse)
async def process_registration(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Регистрирует нового пользователя
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
        new_user = UserCreate(name=name, email=email, hashed_password=hashed_password)
        await create_user(session, new_user)
        response = RedirectResponse("/login", status_code=303)

        return response

    else:
        return templates.TemplateResponse(
            "register.html", {"request": request, "form": form}
        )


@router.get("/login", response_class=HTMLResponse)
async def show_login_form(
    request: Request,
    token=Cookie(default=None),
):
    if token:
        return RedirectResponse("/users/home")

    form = LoginForm()
    return templates.TemplateResponse(
        name="login.html", context={"request": request, "form": form}
    )


@router.post("/login", response_class=HTMLResponse)
async def process_login(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_getter),
):
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
    request: Request,
    user=Depends(check_auth),
):
    response = RedirectResponse("/login")
    response.delete_cookie(key="token", httponly=True)

    return response


@router.get("/users/home", response_class=HTMLResponse)
async def user_page(
    request: Request,
    user=Depends(check_auth),
):
    return templates.TemplateResponse(
        name="user_page.html", context={"request": request, "name": user.name}
    )
