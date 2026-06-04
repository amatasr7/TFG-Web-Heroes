"""Seeder for Ability table."""

from sqlalchemy.orm import Session

from app.ddbb.Models.Ability import Ability

ABILITIES_DATA = [
    {
        "slug": "golpe_brutal",
        "name": "Golpe Brutal",
        "class_name": "Guerrero",
        "mp_cost": 1,
        "effect_type": "damage_single",
        "damage_multiplier": 1.5,
        "flat_damage": None,
        "guaranteed_hit": True,
    },
    {
        "slug": "grito_de_guerra",
        "name": "Grito de Guerra",
        "class_name": "Guerrero",
        "mp_cost": 1,
        "effect_type": "heavy_defend",
        "damage_multiplier": None,
        "flat_damage": None,
        "guaranteed_hit": False,
    },
    {
        "slug": "bola_de_fuego",
        "name": "Bola de Fuego",
        "class_name": "Mago",
        "mp_cost": 4,
        "effect_type": "damage_all",
        "damage_multiplier": None,
        "flat_damage": 3,
        "guaranteed_hit": True,
    },
    {
        "slug": "rayo_de_hielo",
        "name": "Rayo de Hielo",
        "class_name": "Mago",
        "mp_cost": 2,
        "effect_type": "damage_pierce",
        "damage_multiplier": None,
        "flat_damage": 4,
        "guaranteed_hit": True,
    },
    {
        "slug": "golpe_furtivo",
        "name": "Golpe Furtivo",
        "class_name": "Picaro",
        "mp_cost": 2,
        "effect_type": "damage_single",
        "damage_multiplier": 2.0,
        "flat_damage": None,
        "guaranteed_hit": True,
    },
    {
        "slug": "evasion",
        "name": "Evasión",
        "class_name": "Picaro",
        "mp_cost": 1,
        "effect_type": "evasion",
        "damage_multiplier": None,
        "flat_damage": None,
        "guaranteed_hit": False,
    },
]


def seed_abilities(db: Session) -> None:
    """Seed abilities table."""
    for data in ABILITIES_DATA:
        db.add(Ability(**data))
    db.flush()
