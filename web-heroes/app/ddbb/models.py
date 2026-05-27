from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ddbb.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), default="")
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    heroes: Mapped[list["Hero"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class HeroClass(Base):
    __tablename__ = "hero_classes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    base_hp_max: Mapped[int] = mapped_column(Integer, default=10)
    base_mp_max: Mapped[int] = mapped_column(Integer, default=10)
    default_race: Mapped[str] = mapped_column(String(255), default="Criatura")
    adjectives: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    is_playable: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    heroes: Mapped[list["Hero"]] = relationship(back_populates="hero_class")
    enemies: Mapped[list["Enemy"]] = relationship(back_populates="hero_class")


class Hero(Base):
    __tablename__ = "heroes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    hero_class_id: Mapped[int] = mapped_column(ForeignKey("hero_classes.id"))
    name: Mapped[str] = mapped_column(String(255))
    hp_current: Mapped[int] = mapped_column(Integer, default=10)
    mp_current: Mapped[int] = mapped_column(Integer, default=10)
    energy_current: Mapped[int] = mapped_column(Integer, default=10)
    experience: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    last_regen_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="heroes")
    hero_class: Mapped[HeroClass] = relationship(back_populates="heroes")
    hero_items: Mapped[list["HeroItem"]] = relationship(back_populates="hero", cascade="all, delete-orphan")


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


class ItemType(Base):
    __tablename__ = "item_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items: Mapped[list["Item"]] = relationship(back_populates="type")


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
