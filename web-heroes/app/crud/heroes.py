import random
from datetime import datetime

from sqlalchemy.orm import Session, joinedload, selectinload

from app.crud import base
from app.ddbb.Models import Hero, HeroItem, Item
from app.schemas.hero import HeroCreate, HeroUpdate

ENERGY_MAX = 10
XP_PER_LEVEL = 100

_CLASS_STARTING_WEAPON = {
    "Guerrero": "Hacha de hierro",
    "Mago": "Espada de hierro",
    "Picaro": "Arco de hierro",
}


def _hero_options():
    return [
        joinedload(Hero.hero_class),
        selectinload(Hero.hero_items).joinedload(HeroItem.item).joinedload(Item.type),
    ]


def list_heroes(db: Session, user_id: int | None = None) -> list[Hero]:
    query = db.query(Hero).options(*_hero_options())
    if user_id is not None:
        query = query.filter(Hero.user_id == user_id)
    return query.order_by(Hero.id).all()


def get_hero(db: Session, hero_id: int) -> Hero | None:
    return (
        db.query(Hero)
        .options(*_hero_options())
        .filter(Hero.id == hero_id)
        .first()
    )


def create_hero(db: Session, payload: HeroCreate) -> Hero:
    from app.ddbb.Models import HeroClass
    hero_class = db.query(HeroClass).filter(HeroClass.id == payload.hero_class_id).first()
    if not hero_class:
        raise ValueError(f"HeroClass with id {payload.hero_class_id} not found")
    hero_data = payload.model_dump(exclude_none=True)
    if "attack" not in hero_data:
        hero_data["attack"] = hero_class.base_attack
    if "defense" not in hero_data:
        hero_data["defense"] = hero_class.base_defense
    if "hp_current" not in hero_data:
        hero_data["hp_current"] = hero_class.base_hp_max
    if "mp_current" not in hero_data:
        hero_data["mp_current"] = hero_class.base_mp_max
    hero = Hero(**hero_data)
    db.add(hero)
    db.commit()
    db.refresh(hero)
    hero = get_hero(db, hero.id)
    equip_starting_items(db, hero)
    db.commit()
    return get_hero(db, hero.id)


def equip_starting_items(db: Session, hero: Hero) -> None:
    """Equip leather armor + class-appropriate weapon to a newly created hero."""
    weapon_name = _CLASS_STARTING_WEAPON.get(hero.hero_class.name)
    names = ["Armadura de cuero"]
    if weapon_name:
        names.append(weapon_name)
    items = db.query(Item).filter(Item.name.in_(names)).all()
    for item in items:
        db.add(HeroItem(hero_id=hero.id, item_id=item.id, item_type_id=item.item_type_id))


def update_hero(db: Session, hero: Hero, payload: HeroUpdate) -> Hero:
    updated = base.update(db, hero, payload)
    return get_hero(db, updated.id)


def delete_hero(db: Session, hero: Hero) -> None:
    base.delete(db, hero)


def _hp_max(hero: Hero) -> int:
    return hero.hero_class.base_hp_max + hero.hp_bonus


def _mp_max(hero: Hero) -> int:
    return hero.hero_class.base_mp_max + hero.mp_bonus


def refresh_hero_stats(db: Session, hero: Hero) -> Hero:
    now = datetime.utcnow()
    minutes_passed = int((now - hero.last_regen_at).total_seconds() // 60)
    if minutes_passed <= 0:
        return hero
    regen_amount = minutes_passed // 10
    if regen_amount <= 0:
        return hero

    hero.hp_current = min(_hp_max(hero), hero.hp_current + regen_amount)
    hero.mp_current = min(_mp_max(hero), hero.mp_current + regen_amount)
    hero.energy_current = min(ENERGY_MAX, hero.energy_current + regen_amount)
    hero.last_regen_at = now
    db.commit()
    db.refresh(hero)
    return hero


def add_experience(db: Session, hero: Hero, amount: int) -> dict:
    """Add XP. Does NOT auto-level — the user must level up manually."""
    hero.experience += amount
    db.commit()
    db.refresh(hero)
    return {
        "xp_gained": amount,
        "current_xp": hero.experience,
        "level": hero.level,
        "leveled_up": False,
        "can_level_up": hero.experience >= XP_PER_LEVEL,
    }


# ── Hero actions ──────────────────────────────────────────────────────────────

def rest_hero(db: Session, hero: Hero) -> Hero:
    """Restore energy to maximum."""
    hero.energy_current = ENERGY_MAX
    db.commit()
    db.refresh(hero)
    return get_hero(db, hero.id)


def level_up_hero(db: Session, hero: Hero, stat: str) -> Hero:
    """
    Consume 100 XP, increment level, and boost the chosen stat.
    stat must be one of: 'hp', 'mp', 'attack', 'defense'.
    Raises ValueError if not enough XP or unknown stat.
    """
    if hero.experience < XP_PER_LEVEL:
        raise ValueError("El héroe no tiene suficiente experiencia para subir de nivel.")

    hero.experience -= XP_PER_LEVEL
    hero.level += 1

    if stat == "hp":
        hero.hp_bonus += 2
        hero.hp_current = _hp_max(hero)
    elif stat == "mp":
        hero.mp_bonus += 2
        hero.mp_current = _mp_max(hero)
    elif stat == "attack":
        hero.attack += 1
    elif stat == "defense":
        hero.defense += 1
    else:
        raise ValueError(f"Estadística desconocida: {stat}")

    db.commit()
    db.refresh(hero)
    return get_hero(db, hero.id)


ACTION_COOLDOWNS: dict[str, int] = {
    "meditate": 30,
    "train": 60,
    "steal": 30,
}


def check_action_cooldown(hero: Hero, action: str) -> int:
    """Return remaining cooldown in minutes, or 0 if the action is available."""
    cooldown_minutes = ACTION_COOLDOWNS.get(action, 0)
    if cooldown_minutes == 0 or hero.last_action_at is None:
        return 0
    elapsed = (datetime.utcnow() - hero.last_action_at).total_seconds() / 60
    remaining = cooldown_minutes - elapsed
    return max(0, int(remaining))


def meditate_hero(db: Session, hero: Hero) -> Hero:
    """Restore MP to maximum (Mago action)."""
    hero.mp_current = _mp_max(hero)
    hero.last_action_at = datetime.utcnow()
    db.commit()
    db.refresh(hero)
    return get_hero(db, hero.id)


def train_hero(db: Session, hero: Hero) -> Hero:
    """Permanently increase defense by 1 (Guerrero action)."""
    hero.defense += 1
    hero.last_action_at = datetime.utcnow()
    db.commit()
    db.refresh(hero)
    return get_hero(db, hero.id)


def steal_hero(db: Session, hero: Hero, user_id: int) -> dict:
    """Award random 5-15 gold to the user (Pícaro action)."""
    from app.ddbb.Models import User
    user = db.get(User, user_id)
    if user is None:
        raise ValueError("Usuario no encontrado.")
    gold = random.randint(5, 15)
    user.gold += gold
    hero.last_action_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return {"gold_gained": gold, "new_gold": user.gold}
