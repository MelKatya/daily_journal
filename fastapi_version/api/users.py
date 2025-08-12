from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.utils import check_auth
from core.models import db_helper
from core.schemas.users import UserCreate, UserCreateRead, UserLogin
from crud.user import create_user, check_name_exists
from security.utils import get_password_hash, verify_password, create_jwt_token

router = APIRouter(
    tags=["Users"]
)


@router.post("/registration")
async def registers_new_user(
    user_read: UserCreateRead,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Регистрирует нового пользователя
    """
    hashed_password = get_password_hash(user_read.password)
    new_user = UserCreate(name=user_read.name, email=user_read.email, hashed_password=hashed_password)
    user = await create_user(session, new_user)
    return user


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
