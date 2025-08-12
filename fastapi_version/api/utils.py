from fastapi import HTTPException, status, Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from crud.user import get_user_by_id
from security.utils import get_user_id_from_token


async def check_auth(
    token=Cookie(),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Проверяет, что токен есть в cookie и существование пользователя по ID.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )

    user_id = get_user_id_from_token(token)
    if not (user := await get_user_by_id(session, user_id)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with id={user_id} not found",
        )

    return user
