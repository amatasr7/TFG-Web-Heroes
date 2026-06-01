from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.hero_class import HeroClassRead


class HeroBase(BaseModel):
    user_id: int
    hero_class_id: int
    name: str
    sprite_id: str
    hp_current: int = 10
    mp_current: int = 10
    energy_current: int = 10
    experience: int = 0
    level: int = 1
    last_regen_at: datetime | None = None


class HeroCreate(HeroBase):
    pass


class HeroUpdate(BaseModel):
    user_id: int | None = None
    hero_class_id: int | None = None
    name: str | None = None
    hp_current: int | None = None
    mp_current: int | None = None
    energy_current: int | None = None
    experience: int | None = None
    level: int | None = None
    last_regen_at: datetime | None = None


class HeroRead(HeroBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hero_class: HeroClassRead = Field(alias="hero_class")
