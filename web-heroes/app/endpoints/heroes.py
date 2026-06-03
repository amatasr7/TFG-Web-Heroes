from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.heroes import (
    ACTION_COOLDOWNS,
    check_action_cooldown,
    create_hero,
    delete_hero,
    get_hero,
    level_up_hero,
    list_heroes,
    meditate_hero,
    refresh_hero_stats,
    rest_hero,
    steal_hero,
    train_hero,
    update_hero,
)
from app.ddbb.database import get_db
from app.endpoints.errors import raise_integrity_error
from app.schemas.hero import HeroCreate, HeroRead, HeroUpdate

router = APIRouter(tags=["heroes"])


class LevelUpPayload(BaseModel):
    stat: str  # "hp" | "mp" | "attack" | "defense"


class ActionPayload(BaseModel):
    action: str   # "meditate" | "train" | "steal"
    user_id: int | None = None


@router.get("/heroes", response_model=list[HeroRead])
def index(user_id: int | None = None, db: Session = Depends(get_db)):
    return list_heroes(db, user_id)


@router.get("/heroes/{hero_id}", response_model=HeroRead)
def show(hero_id: int, db: Session = Depends(get_db)):
    hero = get_hero(db, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado.")
    return refresh_hero_stats(db, hero)


@router.post("/heroes", response_model=HeroRead, status_code=status.HTTP_201_CREATED)
def store(payload: HeroCreate, db: Session = Depends(get_db)):
    try:
        return create_hero(db, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.put("/heroes/{hero_id}", response_model=HeroRead)
def replace(hero_id: int, payload: HeroUpdate, db: Session = Depends(get_db)):
    hero = get_hero(db, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado.")
    try:
        return update_hero(db, hero, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.patch("/heroes/{hero_id}", response_model=HeroRead)
def patch(hero_id: int, payload: HeroUpdate, db: Session = Depends(get_db)):
    return replace(hero_id, payload, db)


@router.delete("/heroes/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(hero_id: int, db: Session = Depends(get_db)):
    hero = get_hero(db, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado.")
    try:
        delete_hero(db, hero)
    except IntegrityError as error:
        raise_integrity_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/heroes/{hero_id}/rest", response_model=HeroRead)
def rest(hero_id: int, db: Session = Depends(get_db)):
    """Restore hero energy to maximum."""
    hero = get_hero(db, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado.")
    return rest_hero(db, hero)


@router.post("/heroes/{hero_id}/level-up", response_model=HeroRead)
def level_up(hero_id: int, payload: LevelUpPayload, db: Session = Depends(get_db)):
    """Manually level up a hero, choosing which stat to increase."""
    hero = get_hero(db, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado.")
    try:
        return level_up_hero(db, hero, payload.stat)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/heroes/{hero_id}/action")
def class_action(hero_id: int, payload: ActionPayload, db: Session = Depends(get_db)):
    """Execute a class-specific action (meditate, train, steal)."""
    hero = get_hero(db, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado.")

    # Cooldown check
    remaining = check_action_cooldown(hero, payload.action)
    if remaining > 0:
        cooldown_total = ACTION_COOLDOWNS.get(payload.action, 0)
        if remaining >= 60:
            time_str = f"{remaining // 60}h {remaining % 60}min"
        else:
            time_str = f"{remaining} min"
        raise HTTPException(
            status_code=429,
            detail=f"Acción en recarga. Disponible en {time_str}. (Recarga: {cooldown_total} min)",
        )

    try:
        if payload.action == "meditate":
            updated = meditate_hero(db, hero)
            return {"hero": HeroRead.model_validate(updated), "message": f"{hero.name} medita y recupera su maná."}

        if payload.action == "train":
            updated = train_hero(db, hero)
            return {"hero": HeroRead.model_validate(updated), "message": f"{hero.name} entrena y su defensa aumenta."}

        if payload.action == "steal":
            if not payload.user_id:
                raise HTTPException(status_code=400, detail="user_id requerido para robar.")
            result = steal_hero(db, hero, payload.user_id)
            updated = get_hero(db, hero_id)
            return {
                "hero": HeroRead.model_validate(updated),
                "message": f"{hero.name} roba {result['gold_gained']} de oro.",
                "gold_gained": result["gold_gained"],
                "new_gold": result["new_gold"],
            }

        raise HTTPException(status_code=400, detail=f"Acción desconocida: {payload.action}")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
