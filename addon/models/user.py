from __future__ import annotations

from datetime import datetime, timezone
from secrets import token_hex

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from addon.models.meta import Base, DateTimeTzAware


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(32), default=lambda: token_hex(16), primary_key=True
    )
    created: Mapped[datetime] = mapped_column(
        DateTimeTzAware(),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated: Mapped[datetime] = mapped_column(
        DateTimeTzAware(),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    def log(self):
        return f"USER_{self.name}"
