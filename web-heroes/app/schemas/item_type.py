from pydantic import BaseModel, ConfigDict


class ItemTypeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str


class ItemTypeCreate(BaseModel):
    name: str
    slug: str


class ItemTypeUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
