from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ddbb.database import Base

if TYPE_CHECKING:
    from app.ddbb.Models.ItemType import ItemType
    from app.ddbb.Models.ShopItem import ShopItem
    from app.ddbb.Models.UserItem import UserItem

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    item_type_id: Mapped[int] = mapped_column(ForeignKey("item_types.id"))
    sprite_x: Mapped[int] = mapped_column(Integer, default=0)
    sprite_y: Mapped[int] = mapped_column(Integer, default=0)
    hp_bonus: Mapped[int] = mapped_column(Integer, default=0)
    mp_bonus: Mapped[int] = mapped_column(Integer, default=0)
    damage_bonus: Mapped[int] = mapped_column(Integer, default=0)
    price: Mapped[int] = mapped_column(Integer, default=0)
    value: Mapped[int] = mapped_column(Integer, default=0)
    thumbnail_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    type: Mapped[ItemType] = relationship(back_populates="items")
    hero_items: Mapped[list["HeroItem"]] = relationship(back_populates="item")
    shop_items: Mapped[list["ShopItem"]] = relationship(back_populates="item")
    user_items: Mapped[list["UserItem"]] = relationship(back_populates="item")