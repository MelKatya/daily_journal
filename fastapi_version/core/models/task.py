from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, ForeignKey, VARCHAR, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Task(Base):

    id_users: Mapped[str] = mapped_column(
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
        server_default=func.now(),
    )
    completed_at: Mapped[datetime]

    users: Mapped["User"] = relationship(back_populates="tasks")
