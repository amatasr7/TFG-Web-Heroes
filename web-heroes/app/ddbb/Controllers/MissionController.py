"""Mission business logic: availability filtering, completion rewards."""
from sqlalchemy.orm import Session

from app.crud.heroes import add_experience, get_hero
from app.crud.missions import count_missions, get_mission, list_missions
from app.crud.user_items import create_user_item, get_user_item, update_user_item_quantity
from app.crud.user_missions import (
    count_completed_missions,
    get_completed_mission_ids,
    mark_mission_completed,
)
from app.ddbb.Models import Item, Mission, User


def get_available_missions(
    db: Session,
    user_id: int | None,
    page: int,
    page_size: int,
) -> dict:
    completed_ids = get_completed_mission_ids(db, user_id) if user_id else []
    guild_rank = count_completed_missions(db, user_id) if user_id else 0
    offset = (page - 1) * page_size
    missions = list_missions(db, offset=offset, limit=page_size, exclude_ids=completed_ids)
    total = count_missions(db, exclude_ids=completed_ids)
    return {
        "missions": missions,
        "page": page,
        "page_size": page_size,
        "total": total,
        "guild_rank": guild_rank,
    }


def get_mission_by_id(db: Session, mission_id: int) -> Mission | None:
    return get_mission(db, mission_id)


def complete_mission(db: Session, mission_id: int, user_id: int, hero_ids: list[int]) -> dict:
    mission = get_mission(db, mission_id)
    if mission is None:
        raise ValueError("Misión no encontrada.")

    user = db.get(User, user_id)
    if user is None:
        raise ValueError("Usuario no encontrado.")

    mark_mission_completed(db, user_id, mission_id)
    user.gold += mission.gold_reward
    db.commit()
    db.refresh(user)

    for hero_id in hero_ids:
        hero = get_hero(db, hero_id)
        if hero:
            add_experience(db, hero, mission.xp_reward)

    items_awarded = []
    for item_id in (mission.item_reward_ids or []):
        item = db.get(Item, item_id)
        if item is None:
            continue
        existing = get_user_item(db, user_id, item_id)
        if existing:
            update_user_item_quantity(db, existing, existing.quantity + 1)
        else:
            create_user_item(db, user_id, item_id, 1)
        items_awarded.append({
            "id": item_id,
            "name": item.name,
            "sprite_x": item.sprite_x,
            "sprite_y": item.sprite_y,
        })

    guild_rank = count_completed_missions(db, user_id)

    return {
        "gold_awarded": mission.gold_reward,
        "xp_awarded": mission.xp_reward,
        "items_awarded": items_awarded,
        "new_gold": user.gold,
        "guild_rank": guild_rank,
    }
