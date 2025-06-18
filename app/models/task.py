from datetime import date, datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Date, Boolean, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from enums.tasks import ImportanceStatusTask

if TYPE_CHECKING:
    from user import User

class Task(Base):
    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None]
    created_date: Mapped[date] = mapped_column(Date, default=datetime.now(timezone.utc))
    finished_date: Mapped[date] = mapped_column(Date)
    importance_status: Mapped[ImportanceStatusTask] = mapped_column(Enum(ImportanceStatusTask))
    complete_status: Mapped[bool] = mapped_column(Boolean)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="tasks")