from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ddbb.database import Base

if TYPE_CHECKING:
    from app.ddbb.Models.HeroClass import HeroClass

class Enemy(Base):
    __tablename__ = "enemies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    hero_class_id: Mapped[int] = mapped_column(ForeignKey("hero_classes.id"))
    level: Mapped[int] = mapped_column(Integer, default=1)
    hp_max: Mapped[int] = mapped_column(Integer)
    hp_current: Mapped[int] = mapped_column(Integer, default=10)
    xp_reward: Mapped[int] = mapped_column(Integer, default=50)
    is_boss: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hero_class: Mapped[HeroClass] = relationship(back_populates="enemies")