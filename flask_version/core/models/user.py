from .base import db


def create_users_table():
    """Создает таблицу пользователей"""
    with db.connect() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(20),
                email VARCHAR(30),
                hashed_password varchar(80),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
