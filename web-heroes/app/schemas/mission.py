from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MissionBase(BaseModel):
    name: str
    description: str
    enemy_ids: list[int] = []
    item_reward_ids: list[int] = []
    xp_reward: int = 100
    gold_reward: int = 50


class MissionCreate(MissionBase):
    pass


class MissionUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    enemy_ids: list[int] | None = None
    item_reward_ids: list[int] | None = None
    xp_reward: int | None = None
    gold_reward: int | None = None


class MissionRead(MissionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
