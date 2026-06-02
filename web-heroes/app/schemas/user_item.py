from pydantic import BaseModel, ConfigDict

from app.schemas.item import ItemRead


class UserItemBase(BaseModel):
    item_id: int
    quantity: int = 1


class UserItemCreate(UserItemBase):
    pass


class UserItemUpdate(BaseModel):
    quantity: int | None = None


class UserItemRead(UserItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item: ItemRead
