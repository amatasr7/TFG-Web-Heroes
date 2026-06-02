from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.ddbb.Models.Hero import Hero
from app.ddbb.Models.Warband import Warband
from app.ddbb.Models.WarbandHero import WarbandHero
from app.schemas.warband import WarbandCreate, WarbandUpdate


def list_warbands(db: Session) -> list[Warband]:
    return (
        db.query(Warband)
        .options(joinedload(Warband.entries).joinedload(WarbandHero.hero))
        .order_by(Warband.id)
        .all()
    )


def get_warband(db: Session, warband_id: int) -> Optional[Warband]:
    return (
        db.query(Warband)
        .options(joinedload(Warband.entries).joinedload(WarbandHero.hero))
        .filter(Warband.id == warband_id)
        .first()
    )


def get_warband_by_user(db: Session, user_id: int) -> Optional[Warband]:
    return (
        db.query(Warband)
        .options(joinedload(Warband.entries).joinedload(WarbandHero.hero))
        .filter(Warband.user_id == user_id)
        .first()
    )


def _validate_hero_ids(db: Session, user_id: int, hero_ids: list[int]) -> list[Hero]:
    if len(set(hero_ids)) != len(hero_ids):
        raise ValueError("Duplicate hero IDs are not allowed in a warband.")

    heroes = db.query(Hero).filter(Hero.id.in_(hero_ids)).all()
    if len(heroes) != len(hero_ids):
        raise ValueError("One or more heroes were not found.")

    for hero in heroes:
        if hero.user_id != user_id:
            raise ValueError("All warband heroes must belong to the warband owner.")

    return heroes


def _create_warband_entries(db: Session, warband: Warband, hero_ids: list[int]) -> None:
    db.query(WarbandHero).filter(WarbandHero.warband_id == warband.id).delete(synchronize_session="fetch")
    for slot, hero_id in enumerate(hero_ids, start=1):
        entry = WarbandHero(warband_id=warband.id, hero_id=hero_id, slot=slot)
        db.add(entry)


def create_warband(db: Session, payload: WarbandCreate) -> Warband:
    _validate_hero_ids(db, payload.user_id, payload.hero_ids)

    warband = Warband(user_id=payload.user_id, name=payload.name)
    db.add(warband)
    db.flush()

    _create_warband_entries(db, warband, payload.hero_ids)
    db.commit()
    db.refresh(warband)
    return get_warband(db, warband.id)


def update_warband(db: Session, warband: Warband, payload: WarbandUpdate) -> Warband:
    if payload.name is not None:
        warband.name = payload.name

    if payload.hero_ids is not None:
        _validate_hero_ids(db, warband.user_id, payload.hero_ids)
        _create_warband_entries(db, warband, payload.hero_ids)

    db.commit()
    db.refresh(warband)
    return get_warband(db, warband.id)


def delete_warband(db: Session, warband: Warband) -> Warband:
    db.delete(warband)
    db.commit()
    return warband
