from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ddbb.database import Base

if TYPE_CHECKING:
    from app.ddbb.Models.Hero import Hero
    from app.ddbb.Models.Warband import Warband


class WarbandHero(Base):
    __tablename__ = "warband_heroes"
    __table_args__ = (
        UniqueConstraint("warband_id", "slot"),
        UniqueConstraint("warband_id", "hero_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    warband_id: Mapped[int] = mapped_column(ForeignKey("warbands.id", ondelete="CASCADE"))
    hero_id: Mapped[int] = mapped_column(ForeignKey("heroes.id", ondelete="CASCADE"))
    slot: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    warband: Mapped[Warband] = relationship(back_populates="entries")
    hero: Mapped[Hero] = relationship(back_populates="warband_entry")
