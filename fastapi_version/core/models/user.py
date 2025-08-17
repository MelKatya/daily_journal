from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import VARCHAR, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from task import Task


class User(Base):

    name: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    hashed_password: Mapped[str] = mapped_column(VARCHAR(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default=func.now()
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="users", cascade="all, delete-orphan"
    )
