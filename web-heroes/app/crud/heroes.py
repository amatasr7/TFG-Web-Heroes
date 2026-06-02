from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.crud import base
from app.ddbb.Models import Hero
from app.schemas.hero import HeroCreate, HeroUpdate


def list_heroes(db: Session) -> list[Hero]:
    return db.query(Hero).options(joinedload(Hero.hero_class)).order_by(Hero.id).all()


def get_hero(db: Session, hero_id: int) -> Hero | None:
    return (
        db.query(Hero)
        .options(joinedload(Hero.hero_class))
        .filter(Hero.id == hero_id)
        .first()
    )


def create_hero(db: Session, payload: HeroCreate) -> Hero:
    # Get the hero class to get base attack and defense values
    from app.ddbb.Models import HeroClass
    hero_class = db.query(HeroClass).filter(HeroClass.id == payload.hero_class_id).first()
    
    if not hero_class:
        raise ValueError(f"HeroClass with id {payload.hero_class_id} not found")
    
    # Create hero with base values from hero class
    hero_data = payload.model_dump(exclude_none=True)
    # Always use hero class base values unless explicitly provided
    if 'attack' not in hero_data:
        hero_data['attack'] = hero_class.base_attack
    if 'defense' not in hero_data:
        hero_data['defense'] = hero_class.base_defense
    
    hero = Hero(**hero_data)
    db.add(hero)
    db.commit()
    db.refresh(hero)
    return get_hero(db, hero.id)


def update_hero(db: Session, hero: Hero, payload: HeroUpdate) -> Hero:
    updated = base.update(db, hero, payload)
    return get_hero(db, updated.id)


def delete_hero(db: Session, hero: Hero) -> None:
    base.delete(db, hero)


def refresh_hero_stats(db: Session, hero: Hero) -> Hero:
    now = datetime.utcnow()
    minutes_passed = int((now - hero.last_regen_at).total_seconds() // 60)

    if minutes_passed <= 0:
        return hero

    regen_amount = minutes_passed // 10
    if regen_amount <= 0:
        return hero

    hero.hp_current = min(hero.hero_class.base_hp_max, hero.hp_current + regen_amount)
    hero.mp_current = min(hero.hero_class.base_mp_max, hero.mp_current + regen_amount)
    hero.energy_current = min(10, hero.energy_current + regen_amount)
    hero.last_regen_at = now
    db.commit()
    db.refresh(hero)
    return hero


def add_experience(db: Session, hero: Hero, amount: int) -> dict[str, int | bool]:
    hero.experience += amount
    leveled_up = False

    if hero.experience >= 100:
        hero.level += 1
        hero.experience -= 100
        hero.hp_current = hero.hero_class.base_hp_max
        leveled_up = True

    db.commit()
    db.refresh(hero)
    return {
        "xp_gained": amount,
        "current_xp": hero.experience,
        "level": hero.level,
        "leveled_up": leveled_up,
    }
