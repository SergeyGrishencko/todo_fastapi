from typing import TYPE_CHECKING
from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from task import Task

class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    tasks: Mapped[list["Task"]] = relationship(back_populates="user")