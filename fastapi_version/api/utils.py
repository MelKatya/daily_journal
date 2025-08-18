from core.models import User, db_helper
from crud.user import get_user_by_id
from fastapi import Cookie, Depends, HTTPException, Request
from security.utils import get_user_id_from_token
from sqlalchemy.ext.asyncio import AsyncSession


async def check_auth(
    request: Request,
    token=Cookie(default=None),  # noqa B008
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa B008
) -> User | None:
    """
    Проверяет наличие токена в cookie и существование пользователя по ID.

    Args:
        request (Request): объект запроса FastAPI.
        token (str | None): JWT-токен из cookie; None, если токен отсутствует.
        session (AsyncSession): асинхронная сессия SQLAlchemy.

    Returns:
        User | None: объект пользователя, если токен валиден и пользователь
        существует, иначе вызывает HTTPException с редиректом на /login.
    """
    if not token:
        raise HTTPException(status_code=303, headers={"Location": "/login"})

    user_id = get_user_id_from_token(token)
    assert isinstance(user_id, int)
    if not (user := await get_user_by_id(session, user_id)):
        raise HTTPException(status_code=303, headers={"Location": "/login"})

    return user
