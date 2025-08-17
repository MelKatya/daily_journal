from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.users import UserCreate


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
) -> User:
    """
    Добавляет нового пользователя в таблицу 'users'.

    Args:
        session (AsyncSession): асинхронная сессия SQLAlchemy.
        user_create (UserCreate): объект с данными нового пользователя.

    Returns:
        User: объект созданного пользователя с актуальными полями.
    """
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    return user


async def check_name_exists(
    session: AsyncSession,
    username: str,
) -> User | None:
    """
    Проверяет, существует ли пользователь с указанным именем.

    Args:
        session (AsyncSession): асинхронная сессия SQLAlchemy.
        username (str): имя пользователя для проверки.

    Returns:
        User | None: объект найденного пользователя, если такой существует,
            иначе None.
    """
    stmt = select(User).filter_by(name=username)
    result = await session.scalars(stmt)
    return result.one_or_none()


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    """
    Возвращает пользователя по указанному ID, если такой существует.

    Args:
        session (AsyncSession): асинхронная сессия SQLAlchemy.
        user_id (int): ID пользователя для поиска.

    Returns:
        User | None: объект найденного пользователя, если найден, иначе None.
    """
    stmt = select(User).filter_by(id=user_id)
    result = await session.scalars(stmt)
    return result.one_or_none()
