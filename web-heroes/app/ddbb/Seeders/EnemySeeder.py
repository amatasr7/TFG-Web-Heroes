"""Seeder for Enemy table."""

from sqlalchemy.orm import Session

from app.ddbb.Models import Enemy, HeroClass


ENEMY_SEEDS = [
    {
        "name": "Guerrero enemigo",
        "class_name": "Guerrero",
        "level": 1,
        "hp_max": 8,
        "hp_current": 8,
        "xp_reward": 20,
        "is_boss": False,
    },
    {
        "name": "Chaman enemigo",
        "class_name": "Mago",
        "level": 1,
        "hp_max": 6,
        "hp_current": 6,
        "xp_reward": 25,
        "is_boss": False,
    },
    {
        "name": "Dragon rojo",
        "class_name": "Jefe",
        "level": 5,
        "hp_max": 30,
        "hp_current": 30,
        "xp_reward": 100,
        "is_boss": True,
    },
]


def seed_enemies(db: Session, classes: dict[str, HeroClass]) -> list[Enemy]:
    """
    Seed enemies table.
    
    Args:
        db: Database session
        classes: Dictionary mapping class names to HeroClass instances
        
    Returns:
        List of created Enemy instances
    """
    enemies = []
    
    for enemy_data in ENEMY_SEEDS:
        class_name = enemy_data.pop("class_name")
        hero_class = classes[class_name]
        
        enemy = Enemy(
            hero_class_id=hero_class.id,
            **enemy_data
        )
        db.add(enemy)
        enemies.append(enemy)
    
    db.flush()
    return enemies
