"""Warband business logic: group management and XP distribution."""
from sqlalchemy.orm import Session

from app.crud.heroes import add_experience, get_hero
from app.crud.warbands import (
    create_warband,
    delete_warband,
    get_warband,
    get_warband_by_user,
    list_warbands,
    update_warband,
)
from app.ddbb.Models.Warband import Warband
from app.schemas.warband import WarbandCreate, WarbandUpdate


def list_all_warbands(db: Session) -> list[Warband]:
    return list_warbands(db)


def get_warband_by_id(db: Session, warband_id: int) -> Warband | None:
    return get_warband(db, warband_id)


def get_user_warband(db: Session, user_id: int) -> Warband | None:
    return get_warband_by_user(db, user_id)


def create_new_warband(db: Session, payload: WarbandCreate) -> Warband:
    return create_warband(db, payload)


def update_existing_warband(db: Session, warband: Warband, payload: WarbandUpdate) -> Warband:
    return update_warband(db, warband, payload)


def delete_existing_warband(db: Session, warband: Warband) -> Warband:
    return delete_warband(db, warband)


def award_group_xp(db: Session, hero_ids: list[int], amount: int) -> list[dict]:
    """Award XP to multiple heroes at once (warband-wide distribution)."""
    results = []
    for hero_id in hero_ids:
        hero = get_hero(db, hero_id)
        if hero:
            result = add_experience(db, hero, amount)
            results.append({"hero_id": hero_id, **result})
    return results
