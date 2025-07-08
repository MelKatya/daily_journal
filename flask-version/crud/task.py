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
