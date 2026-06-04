"""Item business logic: equipment management and bonus calculation."""
from sqlalchemy.orm import Session

from app.crud.hero_items import (
    create_hero_item,
    delete_hero_item,
    get_hero_item,
    list_hero_items,
    update_hero_item,
)
from app.ddbb.Models import HeroItem
from app.schemas.hero_item import HeroItemCreate, HeroItemUpdate


def list_equipment(db: Session) -> list[HeroItem]:
    return list_hero_items(db)


def get_equipment_by_id(db: Session, hero_item_id: int) -> HeroItem | None:
    return get_hero_item(db, hero_item_id)


def equip_item(db: Session, payload: HeroItemCreate) -> HeroItem:
    return create_hero_item(db, payload)


def update_equipment(db: Session, hero_item: HeroItem, payload: HeroItemUpdate) -> HeroItem:
    return update_hero_item(db, hero_item, payload)


def unequip_item(db: Session, hero_item: HeroItem) -> None:
    delete_hero_item(db, hero_item)


def calculate_item_bonuses(hero_items: list[HeroItem]) -> dict:
    """Sum all stat bonuses from a hero's equipped items."""
    hp_bonus = sum(hi.item.hp_bonus for hi in hero_items if hi.item)
    mp_bonus = sum(hi.item.mp_bonus for hi in hero_items if hi.item)
    damage_bonus = sum(hi.item.damage_bonus for hi in hero_items if hi.item)
    return {
        "hp_bonus": hp_bonus,
        "mp_bonus": mp_bonus,
        "damage_bonus": damage_bonus,
    }
