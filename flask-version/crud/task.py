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
    """Выводит информацию обо всех задачах авторизованного пользователя"""
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


