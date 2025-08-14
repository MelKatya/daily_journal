from fastapi import HTTPException, Depends, Cookie, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from crud.user import get_user_by_id
from security.utils import get_user_id_from_token


async def check_auth(
    request: Request,
    token=Cookie(default=None),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Проверяет, что токен есть в cookie и существование пользователя по ID.
    """
    if not token:
        raise HTTPException(status_code=303, headers={"Location": "/login"})

    user_id = get_user_id_from_token(token)
    if not (user := await get_user_by_id(session, user_id)):
        raise HTTPException(status_code=303, headers={"Location": "/login"})

    return user
