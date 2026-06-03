from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.combat import handle_hero_attack
from app.crud.enemies import get_enemy
from app.crud.heroes import add_experience, get_hero
from app.ddbb.database import get_db
from app.schemas.combat import CombatResult

router = APIRouter(tags=["combat"])


@router.post("/combat/attack/{hero_id}/{enemy_id}", response_model=CombatResult)
def attack(hero_id: int, enemy_id: int, db: Session = Depends(get_db)):
    hero = get_hero(db, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado.")

    enemy = get_enemy(db, enemy_id)
    if enemy is None:
        raise HTTPException(status_code=404, detail="Enemigo no encontrado.")

    if enemy.hp_current <= 0:
        return JSONResponse(
            status_code=400,
            content={
                "error": "El enemigo ya ha sido derrotado.",
                "status": "overkill",
            },
        )

    if hero.hp_current <= 0:
        return JSONResponse(
            status_code=403,
            content={
                "error": "Estas demasiado debil para pelear. Descansa un poco.",
                "status": "hero_dead",
            },
        )

    return handle_hero_attack(db, hero, enemy)


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
