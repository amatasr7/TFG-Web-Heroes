"""Seeder for HeroClass table."""

from sqlalchemy.orm import Session

from app.ddbb.Models import HeroClass

HERO_CLASSES = [
    {
        "name": "Guerrero",
        "is_playable": True,
        "default_race": "Orco",
        "adjectives": ["Bruto", "Cicatrizado", "Acorazado", ""],
        "base_hp_max": 10,
        "base_mp_max": 2,
        "base_attack": 4,
        "base_defense": 5,
    },
    {
        "name": "Mago",
        "is_playable": True,
        "default_race": "Chaman",
        "adjectives": ["Oscuro", "Ascendente", "Malvado", ""],
        "base_hp_max": 6,
        "base_mp_max": 10,
        "base_attack": 3,
        "base_defense": 3,
    },
    {
        "name": "Picaro",
        "is_playable": True,
        "default_race": "Goblin",
        "adjectives": ["Astuto", "Acechante", "Ratero", ""],
        "base_hp_max": 8,
        "base_mp_max": 5,
        "base_attack": 5,
        "base_defense": 4,
    },
    {
        "name": "Animal",
        "is_playable": False,
        "default_race": "Bestia",
        "adjectives": ["Feroz", "Salvaje", "Indomable", ""],
        "base_hp_max": 8,
        "base_mp_max": 0,
        "base_attack": 6,
        "base_defense": 2,
    },
    {
        "name": "Jefe",
        "is_playable": False,
        "default_race": "Dragon",
        "adjectives": ["Rojo", "Azul", "Negro", ""],
        "base_hp_max": 30,
        "base_mp_max": 15,
        "base_attack": 7,
        "base_defense": 7,
    },
]


def seed_hero_classes(db: Session) -> dict[str, HeroClass]:
    """
    Seed hero classes table.
    
    Returns:
        A dictionary mapping class names to HeroClass instances
    """
    classes: dict[str, HeroClass] = {}
    
    for data in HERO_CLASSES:
        hero_class = HeroClass(**data)
        db.add(hero_class)
        classes[data["name"]] = hero_class
    
    db.flush()
    return classes
