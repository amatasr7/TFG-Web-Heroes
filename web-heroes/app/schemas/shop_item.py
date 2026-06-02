from pydantic import BaseModel, ConfigDict

from app.schemas.item import ItemRead


class ShopItemBase(BaseModel):
    item_id: int
    quantity: int = 0


class ShopItemCreate(ShopItemBase):
    pass


class ShopItemUpdate(BaseModel):
    quantity: int | None = None


class ShopItemRead(ShopItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item: ItemRead
