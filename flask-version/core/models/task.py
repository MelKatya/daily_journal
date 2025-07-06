from .base import db


def create_tasks_table():
    with db.connect() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                id_users INT references users(id),
                name VARCHAR(30),
                describe TEXT,
                completed BOOL DEFAULT false,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                completed_at TIMESTAMP 
            )
            """
        )
