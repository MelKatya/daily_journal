from base import db


def create_tasks_table():
    with db.connect() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXIST tasks (
                id INT PRIMARY KEY,
                id_users INT VARCHAR(20) references users(id),
                name VARCHAR(30),
                describe TEXT,
                completed BOOL DEFAULT false,
                created_at TIMESTAMP DEFAULT CURRENT_TIME, 
                completed_at TIMESTAMP 
            )
            """
        )