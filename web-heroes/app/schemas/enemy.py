from pydantic import BaseModel, ConfigDict, Field

from app.schemas.hero_class import HeroClassRead


class EnemyBase(BaseModel):
    name: str
    hero_class_id: int
    level: int = 1
    hp_max: int
    xp_reward: int = 50
    is_boss: bool = False


class EnemyCreate(EnemyBase):
    pass


class EnemyUpdate(BaseModel):
    name: str | None = None
    hero_class_id: int | None = None
    level: int | None = None
    hp_max: int | None = None
    xp_reward: int | None = None
    is_boss: bool | None = None


class EnemyRead(EnemyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hero_class: HeroClassRead = Field(alias="hero_class")
