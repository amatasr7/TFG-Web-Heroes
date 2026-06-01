from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ddbb.database import Base


class Hero(Base):
    __tablename__ = "heroes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    hero_class_id: Mapped[int] = mapped_column(ForeignKey("hero_classes.id"))
    name: Mapped[str] = mapped_column(String(255))
    hp_current: Mapped[int] = mapped_column(Integer, default=10)
    mp_current: Mapped[int] = mapped_column(Integer, default=10)
    energy_current: Mapped[int] = mapped_column(Integer, default=10)
    attack: Mapped[int] = mapped_column(Integer, default=1)
    defense: Mapped[int] = mapped_column(Integer, default=1)
    experience: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    last_regen_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="heroes")
    hero_class: Mapped[HeroClass] = relationship(back_populates="heroes")
    hero_items: Mapped[list["HeroItem"]] = relationship(back_populates="hero", cascade="all, delete-orphan")