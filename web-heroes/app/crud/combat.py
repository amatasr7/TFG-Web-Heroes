import random
import unicodedata

from sqlalchemy.orm import Session

from app.crud.heroes import add_experience
from app.ddbb.Models import Enemy, Hero


# ── Ability definitions ───────────────────────────────────────────────────────

ABILITIES: dict[str, dict] = {
    # Guerrero
    "golpe_brutal": {
        "class_name": "Guerrero",
        "mp_cost": 1,
        "effect_type": "damage_single",
        "damage_multiplier": 1.5,
        "guaranteed_hit": True,
        "name": "Golpe Brutal",
    },
    "grito_de_guerra": {
        "class_name": "Guerrero",
        "mp_cost": 1,
        "effect_type": "heavy_defend",
        "guaranteed_hit": False,
        "name": "Grito de Guerra",
    },
    # Mago
    "bola_de_fuego": {
        "class_name": "Mago",
        "mp_cost": 4,
        "effect_type": "damage_all",
        "flat_damage": 3,
        "guaranteed_hit": True,
        "name": "Bola de Fuego",
    },
    "rayo_de_hielo": {
        "class_name": "Mago",
        "mp_cost": 2,
        "effect_type": "damage_pierce",
        "flat_damage": 4,
        "guaranteed_hit": True,
        "name": "Rayo de Hielo",
    },
    # Pícaro / Picaro
    "golpe_furtivo": {
        "class_name": "Picaro",
        "mp_cost": 2,
        "effect_type": "damage_single",
        "damage_multiplier": 2.0,
        "guaranteed_hit": True,
        "name": "Golpe Furtivo",
    },
    "evasion": {
        "class_name": "Picaro",
        "mp_cost": 1,
        "effect_type": "evasion",
        "guaranteed_hit": False,
        "name": "Evasión",
    },
}


def _normalize(text: str) -> str:
    return unicodedata.normalize("NFD", text.lower()).encode("ascii", "ignore").decode()


def use_ability(db: Session, hero: Hero, ability_id: str) -> dict:
    """Validate and deduct MP for a hero ability. Returns ability metadata for frontend to apply."""
    ability = ABILITIES.get(ability_id)
    if ability is None:
        raise ValueError(f"Habilidad desconocida: {ability_id}")

    hero_class = _normalize(hero.hero_class.name)
    required_class = _normalize(ability["class_name"])
    if hero_class != required_class:
        raise ValueError(f"{hero.name} no puede usar esa habilidad.")

    if hero.mp_current < ability["mp_cost"]:
        raise ValueError(f"Maná insuficiente. Necesitas {ability['mp_cost']} MP.")

    hero.mp_current -= ability["mp_cost"]
    db.commit()
    db.refresh(hero)

    return {
        "ability_id": ability_id,
        "ability_name": ability["name"],
        "mp_remaining": hero.mp_current,
        "effect_type": ability["effect_type"],
        "damage_multiplier": ability.get("damage_multiplier"),
        "flat_damage": ability.get("flat_damage"),
        "guaranteed_hit": ability.get("guaranteed_hit", False),
    }


def calculate_damage(attacker: Hero) -> int:
    return 3 if attacker.hero_class.name == "Guerrero" else 2


def handle_hero_attack(db: Session, hero: Hero, enemy: Enemy, enemy_hp_current: int) -> dict:
    """Attack an enemy using the HP value provided by the frontend (stateless on enemy side)."""
    combat_log: list[str] = []
    enemy_hp = enemy_hp_current

    if random.randint(1, 100) <= 80:
        damage_to_enemy = calculate_damage(hero)
        enemy_hp -= damage_to_enemy
        combat_log.append(f"{hero.name} ataca a {enemy.name}.")
    else:
        combat_log.append(f"{hero.name} intenta atacar, pero {enemy.name} esquiva el golpe.")

    if enemy_hp > 0:
        if random.randint(1, 100) <= 60:
            hero.hp_current -= 1
            combat_log.append(f"{enemy.name} ataca a {hero.name}.")
        else:
            combat_log.append(f"{enemy.name} intenta contraatacar a {hero.name}, pero falla.")

    rewards = None
    if enemy_hp <= 0:
        enemy_hp = 0
        rewards = add_experience(db, hero, enemy.xp_reward)
        combat_log.append(f"El grupo ha derrotado a {enemy.name}!")
    else:
        db.commit()

    db.refresh(hero)

    return {
        "combat_log": combat_log,
        "hero_status": {
            "hp_remaining": hero.hp_current,
            "is_dead": hero.hp_current <= 0,
        },
        "enemy_status": {
            "hp_remaining": enemy_hp,
            "is_dead": enemy_hp <= 0,
        },
        "rewards": rewards,
    }
