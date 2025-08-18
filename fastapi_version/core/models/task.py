from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import TEXT, VARCHAR, ForeignKey, false, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Task(Base):
    """
    ORM-модель таблицы 'tasks'.

    Поля:
        id (int): первичный ключ.
        id_users (int): внешний ключ на таблицу 'users'.
        name (str): название задачи (макс. 30 символов).
        describe (str): описание задачи.
        created_at (datetime): время создания (по умолчанию текущее).
        completed (bool): статус выполнения (по умолчанию False).
        completed_at(datetime | None): время завершения, если задача выполнена.

    Связи:
        users (User): связь многие-к-одному с таблицей пользователей.
    """

    id_users: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    describe: Mapped[str] = mapped_column(TEXT, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        server_default=func.now(),
    )
    completed: Mapped[bool] = mapped_column(
        default=False,
        server_default=false(),
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    users: Mapped["User"] = relationship(back_populates="tasks")
