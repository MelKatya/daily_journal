from base import db


def create_users_table():
    with db.connect() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXIST users (
                id INT PRIMARY KEY,
                name VARCHAR(20),
                email VARCHAR(30),
                password varchar(80),
                created_at TIMESTAMP DEFAULT CURRENT_TIME 
            )
            """
        )
