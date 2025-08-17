from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.users import UserCreate


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
):
    """
    Добавляет нового пользователя
    """
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    return user


async def check_name_exists(
    session: AsyncSession,
    username: str,
):
    """
    Проверяет существование имени пользователя
    """
    stmt = select(User).filter_by(name=username)
    result = await session.scalars(stmt)
    return result.one_or_none()


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
):
    """Получает пользователя по его ID."""
    stmt = select(User).filter_by(id=user_id)
    result = await session.scalars(stmt)
    return result.one_or_none()
