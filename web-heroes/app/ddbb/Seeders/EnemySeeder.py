"""Seeder for Enemy table."""

from sqlalchemy.orm import Session

from app.ddbb.Models import Enemy, HeroClass


ENEMY_SEEDS = [
    # index 0 — easy
    {
        "name": "Goblin Guerrero",
        "class_name": "Guerrero",
        "level": 1,
        "hp_max": 6,
        "hp_current": 6,
        "xp_reward": 15,
        "is_boss": False,
    },
    # index 1 — easy
    {
        "name": "Goblin Arquero",
        "class_name": "Mago",
        "level": 1,
        "hp_max": 5,
        "hp_current": 5,
        "xp_reward": 15,
        "is_boss": False,
    },
    # index 2 — very easy
    {
        "name": "Slime Verde",
        "class_name": "Mago",
        "level": 1,
        "hp_max": 4,
        "hp_current": 4,
        "xp_reward": 10,
        "is_boss": False,
    },
    # index 3 — medium
    {
        "name": "Orco Guerrero",
        "class_name": "Guerrero",
        "level": 2,
        "hp_max": 10,
        "hp_current": 10,
        "xp_reward": 30,
        "is_boss": False,
    },
    # index 4 — medium
    {
        "name": "Orco Chamán",
        "class_name": "Mago",
        "level": 2,
        "hp_max": 8,
        "hp_current": 8,
        "xp_reward": 35,
        "is_boss": False,
    },
    # index 5 — medium
    {
        "name": "Lobo Salvaje",
        "class_name": "Guerrero",
        "level": 2,
        "hp_max": 7,
        "hp_current": 7,
        "xp_reward": 25,
        "is_boss": False,
    },
    # index 6 — medium
    {
        "name": "Lobo Alfa",
        "class_name": "Guerrero",
        "level": 3,
        "hp_max": 9,
        "hp_current": 9,
        "xp_reward": 35,
        "is_boss": False,
    },
    # index 7 — hard
    {
        "name": "Oso Pardo",
        "class_name": "Guerrero",
        "level": 3,
        "hp_max": 12,
        "hp_current": 12,
        "xp_reward": 40,
        "is_boss": False,
    },
    # index 8 — medium
    {
        "name": "Jabalí Furioso",
        "class_name": "Guerrero",
        "level": 2,
        "hp_max": 8,
        "hp_current": 8,
        "xp_reward": 25,
        "is_boss": False,
    },
    # index 9 — boss
    {
        "name": "Golem de Piedra",
        "class_name": "Jefe",
        "level": 4,
        "hp_max": 20,
        "hp_current": 20,
        "xp_reward": 80,
        "is_boss": True,
    },
    # index 10 — boss
    {
        "name": "Dragon Rojo",
        "class_name": "Jefe",
        "level": 5,
        "hp_max": 30,
        "hp_current": 30,
        "xp_reward": 100,
        "is_boss": True,
    },
]


def seed_enemies(db: Session, classes: dict[str, HeroClass]) -> list[Enemy]:
    enemies = []
    for enemy_data in ENEMY_SEEDS:
        data = dict(enemy_data)
        class_name = data.pop("class_name")
        hero_class = classes[class_name]
        enemy = Enemy(hero_class_id=hero_class.id, **data)
        db.add(enemy)
        enemies.append(enemy)
    db.flush()
    return enemies
