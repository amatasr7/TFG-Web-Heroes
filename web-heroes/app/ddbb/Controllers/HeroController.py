"""Hero business logic: stats calculation, class actions, leveling."""
from pydantic import BaseModel

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
from app.ddbb.Models import Hero
from app.schemas.hero import HeroCreate, HeroRead, HeroUpdate


class CreateWithContractPayload(BaseModel):
    user_id: int
    hero_class_id: int
    name: str
    sprite_url: str | None = None


def get_heroes_for_user(db: Session, user_id: int | None = None) -> list[Hero]:
    return list_heroes(db, user_id)


def get_hero_with_refresh(db: Session, hero_id: int) -> Hero | None:
    hero = get_hero(db, hero_id)
    if hero is None:
        return None
    return refresh_hero_stats(db, hero)


def create_new_hero(db: Session, payload: HeroCreate) -> Hero:
    return create_hero(db, payload)


def update_hero_data(db: Session, hero: Hero, payload: HeroUpdate) -> Hero:
    return update_hero(db, hero, payload)


def delete_hero_record(db: Session, hero: Hero) -> None:
    delete_hero(db, hero)


def rest_hero_energy(db: Session, hero: Hero) -> Hero:
    return rest_hero(db, hero)


def level_up(db: Session, hero: Hero, stat: str) -> Hero:
    return level_up_hero(db, hero, stat)


def calculate_total_stats(hero: Hero) -> dict:
    """Return computed totals including item bonuses."""
    hp_max = hero.hero_class.base_hp_max + hero.hp_bonus
    mp_max = hero.hero_class.base_mp_max + hero.mp_bonus
    attack_bonus = sum(hi.item.damage_bonus for hi in hero.hero_items if hi.item)
    hp_item_bonus = sum(hi.item.hp_bonus for hi in hero.hero_items if hi.item)
    mp_item_bonus = sum(hi.item.mp_bonus for hi in hero.hero_items if hi.item)
    return {
        "hp_max": hp_max,
        "mp_max": mp_max,
        "attack_total": hero.attack + attack_bonus,
        "defense_total": hero.defense,
        "hp_item_bonus": hp_item_bonus,
        "mp_item_bonus": mp_item_bonus,
    }


def execute_class_action(db: Session, hero: Hero, action: str, user_id: int | None = None) -> dict:
    remaining = check_action_cooldown(hero, action)
    if remaining > 0:
        cooldown_total = ACTION_COOLDOWNS.get(action, 0)
        time_str = f"{remaining // 60}h {remaining % 60}min" if remaining >= 60 else f"{remaining} min"
        raise ValueError(f"Acción en recarga. Disponible en {time_str}. (Recarga: {cooldown_total} min)")

    if action == "meditate":
        updated = meditate_hero(db, hero)
        return {"hero": HeroRead.model_validate(updated), "message": f"{hero.name} medita y recupera su maná."}

    if action == "train":
        updated = train_hero(db, hero)
        return {"hero": HeroRead.model_validate(updated), "message": f"{hero.name} entrena y su defensa aumenta."}

    if action == "steal":
        if not user_id:
            raise ValueError("user_id requerido para robar.")
        result = steal_hero(db, hero, user_id)
        updated = get_hero(db, hero.id)
        return {
            "hero": HeroRead.model_validate(updated),
            "message": f"{hero.name} roba {result['gold_gained']} de oro.",
            "gold_gained": result["gold_gained"],
            "new_gold": result["new_gold"],
        }

    raise ValueError(f"Acción desconocida: {action}")


def create_hero_with_contract(db: Session, payload: CreateWithContractPayload) -> Hero:
    """Create a hero consuming one 'Contrato de heroe' from the user's inventory."""
    from app.ddbb.Models.Item import Item
    from app.ddbb.Models.UserItem import UserItem

    contract = db.query(Item).filter(Item.name == "Contrato de heroe").first()
    if not contract:
        raise ValueError("El item 'Contrato de heroe' no existe en el sistema.")

    user_item = (
        db.query(UserItem)
        .filter(UserItem.user_id == payload.user_id, UserItem.item_id == contract.id)
        .first()
    )
    if not user_item or user_item.quantity < 1:
        raise ValueError("No tienes contratos de héroe disponibles.")

    hero = create_hero(
        db,
        HeroCreate(
            user_id=payload.user_id,
            hero_class_id=payload.hero_class_id,
            name=payload.name,
            sprite_url=payload.sprite_url,
        ),
    )

    user_item.quantity -= 1
    if user_item.quantity <= 0:
        db.delete(user_item)
    db.commit()

    return hero
