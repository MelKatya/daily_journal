from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import VARCHAR, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from task import Task


class User(Base):
    """
    ORM-модель таблицы 'users'.

    Поля:
        id (int): первичный ключ.
        name (str): имя пользователя (макс. 20 символов).
        email (str): email пользователя (макс. 30 символов).
        hashed_password (str): захэшированный пароль (макс. 80 символов).
        created_at (datetime): время создания (по умолчанию текущее).

    Связи:
        tasks (list[Task]): связь один-ко-многим с таблицей задач.
    """

    name: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    hashed_password: Mapped[str] = mapped_column(VARCHAR(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default=func.now()
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="users", cascade="all, delete-orphan"
    )
