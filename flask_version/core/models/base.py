from contextlib import contextmanager

from psycopg2 import pool
from psycopg2.extras import RealDictCursor

from core.config import settings


class Database:
    """
    Класс для управления пулом соединений с PostgreSQL с помощью psycopg2.
    """

    def __init__(self, user, password, host, database, minconn=1, maxconn=10):
        """
        Инициализирует пул соединений к PostgreSQL.

        Args:
            user (str): имя пользователя базы данных.
            password (str): пароль пользователя.
            host (str): хост, на котором запущена база данных.
            database (str): название базы данных.
            minconn (int): минимальное число соединений в пуле.
            maxconn (int): максимальное число соединений в пуле.
        """
        self.postgresql_pool = pool.SimpleConnectionPool(
            minconn=minconn,
            maxconn=maxconn,
            user=user,
            password=password,
            host=host,
            database=database,
        )

    @contextmanager
    def connect(self):
        """
        Контекстный менеджер для выполнения SQL-запросов с обычным курсором.

        Возвращает курсор без преобразования результатов в словари.
        Коммитит транзакцию при успехе или делает откат при ошибке.
        """
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

    @contextmanager
    def connect_return_dict(self):
        """
        Контекстный менеджер, возвращающий курсор с результатами в виде
        словаря.

        Использует RealDictCursor для получения результатов в формате dict.
        """
        connection = self.postgresql_pool.getconn()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
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
        """
        Закрывает все соединения в пуле.
        """
        self.postgresql_pool.closeall()


db = Database(
    user=settings.db.user,
    password=settings.db.password,
    host=settings.db.host,
    database=settings.db.database,
)
