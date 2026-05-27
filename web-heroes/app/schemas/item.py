from pydantic import BaseModel, ConfigDict

from app.schemas.item_type import ItemTypeRead


class ItemBase(BaseModel):
    name: str
    item_type_id: int
    sprite_x: int = 0
    sprite_y: int = 0
    hp_bonus: int = 0
    mp_bonus: int = 0
    damage_bonus: int = 0
    price: int = 0
    value: int = 0
    thumbnail_url: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = None
    item_type_id: int | None = None
    sprite_x: int | None = None
    sprite_y: int | None = None
    hp_bonus: int | None = None
    mp_bonus: int | None = None
    damage_bonus: int | None = None
    price: int | None = None
    value: int | None = None
    thumbnail_url: str | None = None


class ItemRead(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: ItemTypeRead
