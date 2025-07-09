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


def get_all_tasks(user_id: int):
    """Выводит информацию обо всех задачах авторизованного пользователя"""
    with db.connect_return_dict() as cur:
        cur.execute(
            """
            SELECT * FROM tasks
            where id_users = %s
            """, (user_id,)
        )
        all_tasks = cur.fetchall()
        all_tasks_dict = [dict(row) for row in all_tasks]
        return all_tasks_dict


def get_task_by_id(user_id: int, task_id: int):
    """Выводит информацию о задаче по id авторизованного пользователя"""
    with db.connect_return_dict() as cur:
        cur.execute(
            """
            SELECT * FROM tasks
            where id_users = %s and id = %s
            """, (user_id, task_id)
        )
        task = cur.fetchone()
        if not task:
            return
        task_dict = dict(task)
        return task_dict


def complete_task_by_id(user_id: int, task_id: int):
    """Помечает задачу выполненной"""
    with db.connect_return_dict() as cur:
        cur.execute(
            """
            UPDATE tasks
            set completed = true, completed_at = CURRENT_TIMESTAMP
            where id_users = %s and id = %s and completed = false
            RETURNING *
            """,
            (user_id, task_id),
        )
        result_execute = cur.fetchone()
        if not result_execute:
            return
        task_dict = dict(result_execute)
        return task_dict


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
        result_execute = cur.fetchone()
        return result_execute


