from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.combat import handle_hero_attack, use_ability
from app.crud.enemies import get_enemy
from app.crud.heroes import add_experience, get_hero
from app.ddbb.Controllers import CombatController
from app.ddbb.database import get_db
from app.ddbb.Models.Ability import Ability
from app.schemas.combat import CombatResult

router = APIRouter(tags=["combat"])


# ── Legacy stateless endpoints (kept for backward compatibility) ───────────────

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
            content={"error": "Estas demasiado debil para pelear. Descansa un poco.", "status": "hero_dead"},
        )
    return handle_hero_attack(db, hero, enemy, payload.enemy_hp_current)


class UseAbilityPayload(BaseModel):
    ability_id: str


@router.post("/combat/use-ability/{hero_id}")
def use_hero_ability(hero_id: int, payload: UseAbilityPayload, db: Session = Depends(get_db)):
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
def list_abilities(db: Session = Depends(get_db)):
    abilities = db.query(Ability).order_by(Ability.id).all()
    return {
        a.slug: {
            "name": a.name,
            "class_name": a.class_name,
            "mp_cost": a.mp_cost,
            "effect_type": a.effect_type,
            "damage_multiplier": a.damage_multiplier,
            "flat_damage": a.flat_damage,
            "guaranteed_hit": a.guaranteed_hit,
        }
        for a in abilities
    }


class AwardXpPayload(BaseModel):
    hero_ids: list[int]
    amount: int


@router.post("/combat/award-xp")
def award_xp(payload: AwardXpPayload, db: Session = Depends(get_db)):
    results = []
    for hero_id in payload.hero_ids:
        hero = get_hero(db, hero_id)
        if hero:
            result = add_experience(db, hero, payload.amount)
            results.append({"hero_id": hero_id, **result})
    return results


# ── Stateful battle session endpoints ─────────────────────────────────────────

class StartBattlePayload(BaseModel):
    user_id: int
    mission_id: int | None = None
    enemy_ids: list[int]


@router.post("/combat/battle/start")
def start_battle(payload: StartBattlePayload, db: Session = Depends(get_db)):
    """Create a battle session, generate turn order and run initial enemy turns."""
    try:
        session, logs = CombatController.start_battle(
            db, payload.user_id, payload.mission_id, payload.enemy_ids
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "session_id": session.id,
        "status": session.status,
        "turn_queue": session.turn_queue,
        "current_turn_index": session.current_turn_index,
        "heroes_state": session.heroes_state,
        "enemies_state": session.enemies_state,
        "new_logs": logs,
    }


class BattleActionPayload(BaseModel):
    action: str  # attack | defend | use_ability | use_item
    hero_id: int
    target_enemy_id: int | None = None
    ability_id: str | None = None
    item_id: int | None = None
    user_id: int | None = None


@router.post("/combat/battle/{session_id}/action")
def battle_action(session_id: int, payload: BattleActionPayload, db: Session = Depends(get_db)):
    """Process a hero action, run any subsequent enemy turns, return new state."""
    session = CombatController.get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Sesión de batalla no encontrada.")
    try:
        state, logs = CombatController.process_hero_action(
            db,
            session,
            payload.action,
            payload.hero_id,
            payload.target_enemy_id,
            payload.ability_id,
            payload.item_id,
            payload.user_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {**state, "new_logs": logs}


@router.get("/combat/battle/{session_id}/state")
def get_battle_state(session_id: int, db: Session = Depends(get_db)):
    """Return the current state of a battle session."""
    session = CombatController.get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")
    return {
        "session_id": session.id,
        "status": session.status,
        "turn_queue": session.turn_queue,
        "current_turn_index": session.current_turn_index,
        "heroes_state": session.heroes_state,
        "enemies_state": session.enemies_state,
    }


@router.post("/combat/battle/{session_id}/abandon")
def abandon_battle(session_id: int, db: Session = Depends(get_db)):
    """Mark a battle session as abandoned."""
    session = CombatController.get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")
    CombatController.abandon_battle(db, session)
    return {"status": "abandoned"}
