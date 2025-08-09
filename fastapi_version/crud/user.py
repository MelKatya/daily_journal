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
