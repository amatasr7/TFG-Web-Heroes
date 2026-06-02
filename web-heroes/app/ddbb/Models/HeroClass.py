from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ddbb.database import Base

class HeroClass(Base):
    __tablename__ = "hero_classes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    base_hp_max: Mapped[int] = mapped_column(Integer, default=10)
    base_mp_max: Mapped[int] = mapped_column(Integer, default=10)
    base_attack: Mapped[int] = mapped_column(Integer, default=5)
    base_defense: Mapped[int] = mapped_column(Integer, default=5)
    default_race: Mapped[str] = mapped_column(String(255), default="Criatura")
    adjectives: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    is_playable: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    heroes: Mapped[list["Hero"]] = relationship(back_populates="hero_class")
    enemies: Mapped[list["Enemy"]] = relationship(back_populates="hero_class")