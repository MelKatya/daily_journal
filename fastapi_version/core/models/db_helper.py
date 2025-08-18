from typing import AsyncGenerator

from core.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DatabaseHelper:
    """
    Инициализирует объект DatabaseHelper.

    Создает асинхронный движок SQLAlchemy и фабрику сессий.

    Args:
        url (str): строка подключения к БД.
        echo (bool): логирование SQL-запросов.
        echo_pool (bool): логирование работы пула соединений.
        pool_size (int): размер пула соединений.
        max_overflow (int): максимальное число дополнительных соединений.
    """

    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        # Фабрика для создания асинхронных сессий SQLAlchemy
        self.session_factory: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(  # noqa E501
                bind=self.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
        )

    async def dispose(self) -> None:
        """
        Освобождает ресурсы и закрывает асинхронный движок SQLAlchemy.
        """
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Асинхронный генератор для предоставления сессий.
        Гарантирует корректное закрытие сессии после использования.
        """
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
