from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.ddbb.database import Base


class Ability(Base):
    __tablename__ = "abilities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    class_name: Mapped[str] = mapped_column(String(100))
    mp_cost: Mapped[int] = mapped_column(Integer, default=0)
    effect_type: Mapped[str] = mapped_column(String(100))
    damage_multiplier: Mapped[float | None] = mapped_column(Float, nullable=True)
    flat_damage: Mapped[int | None] = mapped_column(Integer, nullable=True)
    guaranteed_hit: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
