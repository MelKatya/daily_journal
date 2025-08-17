from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)


class Base(DeclarativeBase):
    """
    Базовый абстрактный класс для ORM-моделей.

    - Автоматически формирует имя таблицы на основе имени
        класса (lowercase + 's').
    - Добавляет первичный ключ 'id'.
    """

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    id: Mapped[int] = mapped_column(primary_key=True)
