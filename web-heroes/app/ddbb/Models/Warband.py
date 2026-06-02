from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ddbb.database import Base

if TYPE_CHECKING:
    from app.ddbb.Models.User import User
    from app.ddbb.Models.WarbandHero import WarbandHero


class Warband(Base):
    __tablename__ = "warbands"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    name: Mapped[str] = mapped_column(String(255), default="Warband")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="warband")
    entries: Mapped[list[WarbandHero]] = relationship(back_populates="warband", cascade="all, delete-orphan")
