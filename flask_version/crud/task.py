from core.models import db


def create_task(id_users: int, name: str, describe: str):
    """Создает новую задачу"""
    with db.connect() as cur:
        cur.execute(
            """
            INSERT INTO tasks (id_users, name, describe)
            VALUES (%s, %s, %s)
            """,
            (id_users, name, describe),
        )


def get_all_tasks(
    user_id: int, sorted_for_db: str, completed: tuple[str], search_query: str
):
    """Выводит информацию обо всех задачах авторизованного пользователя"""
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


def get_task_by_id(user_id: int, task_id: int):
    """Выводит информацию о задаче по id авторизованного пользователя"""
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
            return

        return dict(task)


def complete_task_by_id(user_id: int, task_id: int):
    """Помечает задачу выполненной"""
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
            return

        return dict(result_execute)


def not_completed_task_by_id(user_id: int, task_id: int):
    """Помечает задачу невыполненной"""
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
            return

        return dict(result_execute)


def change_describe_task_by_id(
    user_id: int,
    task_id: int,
    describe: str | None,
):
    """Изменяет описание задачи"""
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
            return

        return dict(result_execute)


def delete_task_by_id(user_id: int, task_id: int):
    """Удаляет задачу"""
    with db.connect() as cur:
        cur.execute(
            """
            DELETE FROM tasks
            where id_users = %s and id = %s
            RETURNING name
            """,
            (user_id, task_id),
        )

        return cur.fetchone()
