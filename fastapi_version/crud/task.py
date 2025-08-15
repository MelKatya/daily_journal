import datetime

from sqlalchemy import select, desc, delete
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
    session: AsyncSession,
):
    """Возвращает список отсортированных и отфильтрованных задач.
    Ищет задачи по названию."""
    stmt = select(Task).\
        where(Task.id_users == id_users, Task.completed.in_(completed), Task.name.ilike(f"%{search_query}%")).\
        order_by(sorted_for_db)
    result = await session.scalars(stmt)
    return result.all()


async def get_task_by_id(
    id_users: int,
    task_id: int,
    session: AsyncSession,
):
    """Возвращает информацию о задаче пользователя по их ID."""
    stmt = select(Task).where(Task.id_users == id_users, Task.id == task_id)
    result = await session.scalars(stmt)
    return result.one_or_none()


async def complete_task_by_id(
    id_users: int,
    task_id: int,
    session: AsyncSession,
):
    """Помечает задачу как выполненную и устанавливает дату ее выполнения."""
    task = await get_task_by_id(id_users, task_id, session)
    task.completed = True
    task.completed_at = datetime.datetime.now()
    await session.commit()


async def not_completed_task_by_id(
    id_users: int,
    task_id: int,
    session: AsyncSession,
):
    """Помечает задачу как невыполненную и удаляет дату ее выполнения."""
    task = await get_task_by_id(id_users, task_id, session)
    task.completed = False
    task.completed_at = None
    await session.commit()


async def change_describe_task_by_id(
    id_users: int,
    task_id: int,
    describe: str,
    session: AsyncSession,
):
    task = await get_task_by_id(id_users, task_id, session)
    task.describe = describe
    await session.commit()


async def delete_task_by_id(id_users: int, task_id: int, session: AsyncSession,):
    stmt = delete(Task).where(Task.id == task_id, Task.id_users == id_users)
    await session.execute(stmt)
    await session.commit()

