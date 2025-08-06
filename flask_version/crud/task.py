from typing import Any

from core.models import db


def create_task(id_users: int, name: str, describe: str) -> None:
    """
    Добавляет новую задачу в таблицу 'tasks'.

    Args:
        id_users (int): ID пользователя, создающего задачу.
        name (str): название задачи.
        describe (str): описание задачи.
    """
    with db.connect() as cur:
        cur.execute(
            """
            INSERT INTO tasks (id_users, name, describe)
            VALUES (%s, %s, %s)
            """,
            (id_users, name, describe),
        )


def get_all_tasks(
    user_id: int,
    sorted_for_db: str,
    completed: tuple[str, ...],
    search_query: str,
) -> list[dict]:
    """
    Возвращает список отсортированных и отфильтрованных задач.
    Ищет задачи по названию.

    Args:
        user_id (int): ID пользователя.
        sorted_for_db (str): поле для сортировки в SQL-запросе.
        completed: (tuple[str, ...]): кортеж со статусами задач для фильтрации.
        search_query (str): поисковая строка (поиск по названию задачи).

    Returns:
        list[dict]: список задач, удовлетворяющих условиям фильтрации и поиска.
    """
    search_query = f"%{search_query}%"
    with db.connect_return_dict() as cur:
        cur.execute(
            f"""
            SELECT * FROM tasks
            WHERE id_users = %s
                AND completed in %s
                AND name ILIKE %s
            ORDER BY {sorted_for_db}
            """,
            (user_id, completed, search_query),
        )
        all_tasks = cur.fetchall()
        return [dict(row) for row in all_tasks]


def get_task_by_id(user_id: int, task_id: int) -> dict[str, Any] | None:
    """
    Возвращает информацию о задаче пользователя по их ID.

    Args:
        user_id (int): ID пользователя.
        task_id (int): ID задачи.

    Returns:
        dict[str, Any] | None: словарь с данными задачи, если найдена,
        иначе None.
    """
    with db.connect_return_dict() as cur:
        cur.execute(
            """
            SELECT * FROM tasks
            where id_users = %s and id = %s
            """,
            (user_id, task_id),
        )
        task = cur.fetchone()
        if not task:
            return None

        return dict(task)


def complete_task_by_id(user_id: int, task_id: int) -> dict[str, Any] | None:
    """
    Помечает задачу как выполненную и устанавливает дату ее выполнения.

    Args:
        user_id (int): ID пользователя.
        task_id (int): ID задачи.

    Returns:
        dict[str, Any] | None: словарь с обновленными данными задачи,
        если задача найдена и ее статус был изменен; иначе None.
    """
    with db.connect_return_dict() as cur:
        cur.execute(
            """
            UPDATE tasks
            SET completed = true, completed_at = CURRENT_TIMESTAMP
            WHERE id_users = %s and id = %s and completed = false
            RETURNING *
            """,
            (user_id, task_id),
        )
        result_execute = cur.fetchone()
        if not result_execute:
            return None

        return dict(result_execute)


def not_completed_task_by_id(
    user_id: int,
    task_id: int,
) -> dict[str, Any] | None:
    """
    Помечает задачу как невыполненную и удаляет дату ее выполнения.

    Args:
        user_id (int): ID пользователя.
        task_id (int): ID задачи.

    Returns:
        dict[str, Any] | None: словарь с обновленными данными задачи,
        если задача найдена и ее статус был изменен; иначе None.
    """
    with db.connect_return_dict() as cur:
        cur.execute(
            """
            UPDATE tasks
            SET completed = false, completed_at = Null
            WHERE id_users = %s and id = %s and completed = true
            RETURNING *
            """,
            (user_id, task_id),
        )
        result_execute = cur.fetchone()
        if not result_execute:
            return None

        return dict(result_execute)


def change_describe_task_by_id(
    user_id: int,
    task_id: int,
    describe: str,
) -> dict[str, Any] | None:
    """
    Обновляет описание задачи по ее ID для конкретного пользователя.

    Args:
        user_id (int): ID пользователя.
        task_id (int): ID задачи.
        describe (str): описание задачи.

    Returns:
        dict[str, Any] | None: словарь с обновленными данными задачи,
        если задача найдена и описание обновлено; иначе None.
    """
    with db.connect_return_dict() as cur:
        cur.execute(
            """
            UPDATE tasks
            set describe = %s
            where id_users = %s and id = %s
            RETURNING *
            """,
            (describe, user_id, task_id),
        )
        result_execute = cur.fetchone()
        if not result_execute:
            return None

        return dict(result_execute)


def delete_task_by_id(user_id: int, task_id: int) -> str | None:
    """
    Удаляет задачу по ее ID для конкретного пользователя.

    Args:
        user_id (int): ID пользователя.
        task_id (int): ID задачи.

    Returns:
        str | None: наименование задачи, если она была найдена и удалена;
        иначе None.
    """
    with db.connect() as cur:
        cur.execute(
            """
            DELETE FROM tasks
            where id_users = %s and id = %s
            RETURNING name
            """,
            (user_id, task_id),
        )

        result = cur.fetchone()
        return result[0] if result else None
