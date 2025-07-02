from contextlib import contextmanager

import psycopg2
from psycopg2 import pool

from core.config import settings


class Database:
    def __init__(self, user, password, host, database, minconn=1, maxconn=10):
        self.postgresql_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=minconn,
            maxconn=maxconn,
            user=user,
            password=password,
            host=host,
            database=database
        )

    @contextmanager
    def connect(self):
        connection = self.postgresql_pool.getconn()
        cursor = connection.cursor()
        try:
            yield cursor
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            self.postgresql_pool.putconn(connection)

    def close_pool(self):
        self.postgresql_pool.closeall()


db = Database(
    user=settings.db.user,
    password=settings.db.password,
    host=settings.db.host,
    database=settings.db.database
)
