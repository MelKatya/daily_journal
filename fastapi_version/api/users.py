from fastapi import APIRouter, Depends, HTTPException, Response, status, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.utils import check_auth
from core.models import db_helper
from core.schemas.users import UserCreate, UserCreateRead, UserLogin, RegistrationForm
from crud.user import create_user, check_name_exists
from security.utils import get_password_hash, verify_password, create_jwt_token

router = APIRouter(tags=["Users"])
# router.mount("/static", StaticFiles(directory="/static"), name="static")


templates = Jinja2Templates(directory="templates")


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
        user = await create_user(session, new_user)

        return templates.TemplateResponse(
            "register.html", {"request": request, "form": form}
        )
    else:
        return {"message": "Пsssssтрирован!"}

# @router.get("/registration", response_class=HTMLResponse)
# async def registers_new_user(
#     request: Request,
#     user_read: UserCreateRead = Form(),
#     session: AsyncSession = Depends(db_helper.session_getter),
# ):
#     """
#     Регистрирует нового пользователя
#     """
#     hashed_password = get_password_hash(user_read.password)
#     new_user = UserCreate(name=user_read.name, email=user_read.email, hashed_password=hashed_password)
#     user = await create_user(session, new_user)
#     return templates.TemplateResponse(
#         request=request, name="register.html", context={"form": user_read}
#     )



@router.post("/login")
async def login_user(
    response: Response,
    user_read: UserLogin,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (user := await check_name_exists(session, user_read.name)):
        raise auth_exception

    if not verify_password(user_read.password, user.hashed_password):
        raise auth_exception

    token = create_jwt_token(user.id)

    response.set_cookie(key="token", value=token, httponly=True)
    return {"user": user, "token": token}


@router.post("/logout")
async def logout_user(
    response: Response,
    user=Depends(check_auth),
):
    response.delete_cookie("token")
    return f"By, {user.name}"


@router.post("/users/home")
async def user_page(user=Depends(check_auth)):
    return user
