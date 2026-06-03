from pydantic import BaseModel, ConfigDict

from app.schemas.item import ItemRead


class HeroItemBase(BaseModel):
    hero_id: int
    item_id: int
    item_type_id: int


class HeroItemCreate(HeroItemBase):
    pass


class HeroItemUpdate(BaseModel):
    hero_id: int | None = None
    item_id: int | None = None
    item_type_id: int | None = None


class HeroItemRead(HeroItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item: ItemRead
