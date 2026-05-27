from pydantic import BaseModel


class CombatHeroStatus(BaseModel):
    hp_remaining: int
    is_dead: bool


class CombatEnemyStatus(BaseModel):
    hp_remaining: int
    is_dead: bool


class CombatRewards(BaseModel):
    xp_gained: int
    current_xp: int
    level: int
    leveled_up: bool


class CombatResult(BaseModel):
    combat_log: list[str]
    hero_status: CombatHeroStatus
    enemy_status: CombatEnemyStatus
    rewards: CombatRewards | None
