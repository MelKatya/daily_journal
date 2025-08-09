from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.users import UserCreate, UserCreateRead
from crud.user import create_user
from security.utils import get_password_hash

router = APIRouter(
    tags=["Users"]
)


@router.post("/registration")
async def registers_new_user(
    user_read: UserCreateRead,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    hashed_password = get_password_hash(user_read.password)
    print(user_read)
    new_user = UserCreate(name=user_read.name, email=user_read.email, hashed_password=hashed_password)
    print(new_user)
    user = await create_user(session, new_user)
    return user





@router.post("/login")
async def login_user():
    ...


@router.post("/logout")
async def logout_user():
    ...


@router.post("/users/home")
async def user_page():
    ...
