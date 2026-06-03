from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.heroes import add_experience, get_hero
from app.crud.missions import count_missions, get_mission, list_missions
from app.crud.user_items import create_user_item, get_user_item, update_user_item_quantity
from app.crud.user_missions import (
    count_completed_missions,
    get_completed_mission_ids,
    mark_mission_completed,
)
from app.ddbb.Models import Item, User
from app.ddbb.database import get_db
from app.schemas.mission import MissionRead


class MissionListResponse(BaseModel):
    missions: list[MissionRead]
    page: int
    page_size: int
    total: int
    guild_rank: int = 0


class MissionCompletePayload(BaseModel):
    user_id: int
    hero_ids: list[int]


router = APIRouter(tags=["missions"])


@router.get("/missions", response_model=MissionListResponse)
def index(
    page: int = Query(1, ge=1),
    page_size: int = Query(3, ge=1, le=50),
    user_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    completed_ids = get_completed_mission_ids(db, user_id) if user_id else []
    guild_rank = count_completed_missions(db, user_id) if user_id else 0

    offset = (page - 1) * page_size
    missions = list_missions(db, offset=offset, limit=page_size, exclude_ids=completed_ids)
    total = count_missions(db, exclude_ids=completed_ids)
    return MissionListResponse(
        missions=missions,
        page=page,
        page_size=page_size,
        total=total,
        guild_rank=guild_rank,
    )


@router.get("/missions/{mission_id}", response_model=MissionRead)
def show(mission_id: int, db: Session = Depends(get_db)):
    mission = get_mission(db, mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Misión no encontrada.")
    return mission


@router.post("/missions/{mission_id}/complete")
def complete_mission(mission_id: int, payload: MissionCompletePayload, db: Session = Depends(get_db)):
    """Award gold, bonus XP and item rewards for completing a mission."""
    mission = get_mission(db, mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Misión no encontrada.")

    user = db.get(User, payload.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # Mark mission completed (idempotent — duplicate calls are safe)
    mark_mission_completed(db, payload.user_id, mission_id)

    # Award gold
    user.gold += mission.gold_reward
    db.commit()
    db.refresh(user)

    # Award bonus mission XP to every hero in the warband
    for hero_id in payload.hero_ids:
        hero = get_hero(db, hero_id)
        if hero:
            add_experience(db, hero, mission.xp_reward)

    # Award item rewards to user inventory
    items_awarded = []
    for item_id in (mission.item_reward_ids or []):
        item = db.get(Item, item_id)
        if item is None:
            continue
        existing = get_user_item(db, payload.user_id, item_id)
        if existing:
            update_user_item_quantity(db, existing, existing.quantity + 1)
        else:
            create_user_item(db, payload.user_id, item_id, 1)
        items_awarded.append({
            "id": item_id,
            "name": item.name,
            "sprite_x": item.sprite_x,
            "sprite_y": item.sprite_y,
        })

    guild_rank = count_completed_missions(db, payload.user_id)

    return {
        "gold_awarded": mission.gold_reward,
        "xp_awarded": mission.xp_reward,
        "items_awarded": items_awarded,
        "new_gold": user.gold,
        "guild_rank": guild_rank,
    }
