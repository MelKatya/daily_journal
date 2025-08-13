from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task
from core.schemas.tasks import TaskCreate


async def create_task(task: TaskCreate, session: AsyncSession):
    """Создает новую задачу"""
    task = Task(**task.model_dump())
    session.add(task)
    await session.commit()
    return task


async def get_all_tasks(
    id_users: int,
    sorted_for_db: str,
    completed: list[bool],
    search_query: str,
    session: AsyncSession
):
    """Возвращает список отсортированных и отфильтрованных задач.
    Ищет задачи по названию."""
    stmt = select(Task).\
        where(Task.id_users == id_users, Task.completed.in_(completed), Task.name.ilike(f"%{search_query}%")).\
        order_by(sorted_for_db)
    result = await session.scalars(stmt)
    return result.all()


