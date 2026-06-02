from pydantic import BaseModel, ConfigDict, Field

from app.schemas.hero import HeroRead


class WarbandHeroBase(BaseModel):
    hero_id: int
    slot: int


class WarbandHeroRead(WarbandHeroBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hero: HeroRead


class WarbandBase(BaseModel):
    user_id: int
    name: str = "Warband"


class WarbandCreate(WarbandBase):
    hero_ids: list[int] = Field(..., min_length=3, max_length=3)


class WarbandUpdate(BaseModel):
    name: str | None = None
    hero_ids: list[int] | None = Field(None, min_length=3, max_length=3)


class WarbandRead(WarbandBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    entries: list[WarbandHeroRead] = Field(default_factory=list)
