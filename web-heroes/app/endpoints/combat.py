from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.combat import ABILITIES, handle_hero_attack, use_ability
from app.crud.enemies import get_enemy
from app.crud.heroes import add_experience, get_hero
from app.ddbb.database import get_db
from app.schemas.combat import CombatResult

router = APIRouter(tags=["combat"])


class AttackPayload(BaseModel):
    enemy_hp_current: int


@router.post("/combat/attack/{hero_id}/{enemy_id}", response_model=CombatResult)
def attack(hero_id: int, enemy_id: int, payload: AttackPayload, db: Session = Depends(get_db)):
    hero = get_hero(db, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado.")

    enemy = get_enemy(db, enemy_id)
    if enemy is None:
        raise HTTPException(status_code=404, detail="Enemigo no encontrado.")

    if hero.hp_current <= 0:
        return JSONResponse(
            status_code=403,
            content={
                "error": "Estas demasiado debil para pelear. Descansa un poco.",
                "status": "hero_dead",
            },
        )

    return handle_hero_attack(db, hero, enemy, payload.enemy_hp_current)


class UseAbilityPayload(BaseModel):
    ability_id: str


@router.post("/combat/use-ability/{hero_id}")
def use_hero_ability(hero_id: int, payload: UseAbilityPayload, db: Session = Depends(get_db)):
    """Validate, deduct MP and return ability metadata. Damage is applied client-side."""
    hero = get_hero(db, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado.")
    if hero.hp_current <= 0:
        raise HTTPException(status_code=403, detail="El héroe está fuera de combate.")
    try:
        return use_ability(db, hero, payload.ability_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/combat/abilities")
def list_abilities():
    """Return all ability definitions (for frontend reference)."""
    return ABILITIES


class AwardXpPayload(BaseModel):
    hero_ids: list[int]
    amount: int


@router.post("/combat/award-xp")
def award_xp(payload: AwardXpPayload, db: Session = Depends(get_db)):
    """Award XP to multiple heroes at once (warband-wide XP distribution)."""
    results = []
    for hero_id in payload.hero_ids:
        hero = get_hero(db, hero_id)
        if hero:
            result = add_experience(db, hero, payload.amount)
            results.append({"hero_id": hero_id, **result})
    return results
