import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task
from core.schemas.tasks import TaskCreate


async def create_task(task: TaskCreate, session: AsyncSession) -> Task:
    """
    Создает новую задачу таблице 'tasks'.

    Args:
        task (TaskCreate): объект с данными новой задачи.
        session (AsyncSession): асинхронная сессия SQLAlchemy.

    Returns:
        Task: объект созданной задачи с актуальными полями.
    """
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
) -> list[Task]:
    """
    Возвращает список отсортированных и отфильтрованных задач.
    Ищет задачи по названию.

    Args:
        id_users (int): ID пользователя.
        sorted_for_db (str): поле для сортировки в SQL-запросе.
        completed: (list[bool]): список со статусами задач для фильтрации.
        search_query (str): поисковая строка (поиск по названию задачи).
        session (AsyncSession): асинхронная сессия SQLAlchemy.

    Returns:
        list[Task]: список задач, удовлетворяющих условиям фильтрации и поиска.
    """
    stmt = (
        select(Task)
        .where(
            Task.id_users == id_users,
            Task.completed.in_(completed),
            Task.name.ilike(f"%{search_query}%"),
        )
        .order_by(sorted_for_db)
    )
    result = await session.scalars(stmt)
    return list(result.all())


async def get_task_by_id(
    id_users: int,
    task_id: int,
    session: AsyncSession,
) -> Task | None:
    """
    Возвращает информацию о задаче пользователя по их ID.

    Args:
        id_users (int): ID пользователя.
        task_id (int): ID задачи.
        session (AsyncSession): асинхронная сессия SQLAlchemy.

    Returns:
        Task | None: словарь с данными задачи, если найдена, иначе None.
    """
    stmt = select(Task).where(Task.id_users == id_users, Task.id == task_id)
    result = await session.scalars(stmt)
    return result.one_or_none()


async def complete_task_by_id(
    id_users: int,
    task_id: int,
    session: AsyncSession,
) -> None:
    """
    Помечает задачу как выполненную и устанавливает дату ее выполнения.

    Args:
        id_users (int): ID пользователя.
        task_id (int): ID задачи.
        session (AsyncSession): асинхронная сессия SQLAlchemy.
    """
    task = await get_task_by_id(id_users, task_id, session)
    task.completed = True
    task.completed_at = datetime.datetime.now()
    await session.commit()


async def not_completed_task_by_id(
    id_users: int,
    task_id: int,
    session: AsyncSession,
) -> None:
    """
    Помечает задачу как невыполненную и удаляет дату ее выполнения.

    Args:
        id_users (int): ID пользователя.
        task_id (int): ID задачи.
        session (AsyncSession): асинхронная сессия SQLAlchemy.
    """
    task = await get_task_by_id(id_users, task_id, session)
    task.completed = False
    task.completed_at = None
    await session.commit()


async def change_describe_task_by_id(
    id_users: int,
    task_id: int,
    describe: str,
    session: AsyncSession,
) -> None:
    """
    Обновляет описание задачи по ее ID для конкретного пользователя.

    Args:
        id_users (int): ID пользователя.
        task_id (int): ID задачи.
        describe (str): описание задачи.
        session (AsyncSession): асинхронная сессия SQLAlchemy.
    """
    task = await get_task_by_id(id_users, task_id, session)
    task.describe = describe
    await session.commit()


async def delete_task_by_id(
    id_users: int,
    task_id: int,
    session: AsyncSession,
) -> None:
    """
    Удаляет задачу по ее ID для конкретного пользователя.

    Args:
        id_users (int): ID пользователя.
        task_id (int): ID задачи.
        session (AsyncSession): асинхронная сессия SQLAlchemy.
    """
    stmt = delete(Task).where(Task.id == task_id, Task.id_users == id_users)
    await session.execute(stmt)
    await session.commit()
