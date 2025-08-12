from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task
from core.schemas.tasks import TaskCreate


async def create_task(task: TaskCreate, session: AsyncSession):
    """Создает новую задачу"""
    task = Task(**task.model_dump())
    session.add(task)
    await session.commit()
    return task

