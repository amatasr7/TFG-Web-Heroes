from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ddbb.database import Base

if TYPE_CHECKING:
    from app.ddbb.Models.Hero import Hero
    from app.ddbb.Models.Item import Item
    from app.ddbb.Models.ItemType import ItemType

class HeroItem(Base):
    __tablename__ = "hero_items"
    __table_args__ = (UniqueConstraint("hero_id", "item_type_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hero_id: Mapped[int] = mapped_column(ForeignKey("heroes.id", ondelete="CASCADE"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"))
    item_type_id: Mapped[int] = mapped_column(ForeignKey("item_types.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hero: Mapped[Hero] = relationship(back_populates="hero_items")
    item: Mapped[Item] = relationship(back_populates="hero_items")
    item_type: Mapped[ItemType] = relationship()