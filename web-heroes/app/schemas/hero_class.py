from pydantic import BaseModel, ConfigDict


class HeroClassBase(BaseModel):
    name: str
    base_hp_max: int = 10
    base_mp_max: int = 10
    base_attack: int = 5
    base_defense: int = 5
    default_race: str = "Criatura"
    adjectives: list[str] | None = None
    is_playable: bool = False


class HeroClassCreate(HeroClassBase):
    pass


class HeroClassUpdate(BaseModel):
    name: str | None = None
    base_hp_max: int | None = None
    base_mp_max: int | None = None
    base_attack: int | None = None
    base_defense: int | None = None
    default_race: str | None = None
    adjectives: list[str] | None = None
    is_playable: bool | None = None


class HeroClassRead(HeroClassBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
