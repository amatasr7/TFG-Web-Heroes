"""Seeder for Hero table."""

from sqlalchemy.orm import Session

from app.ddbb.Models import Hero, HeroClass, User


HERO_SEEDS = [
    ("Aragorn", "Guerrero", 10, 2, 10),
    ("Morgana", "Mago", 6, 10, 10),
    ("Sombra", "Picaro", 8, 5, 10),
]


def seed_heroes(db: Session, user: User, classes: dict[str, HeroClass]) -> None:
    """
    Seed heroes table.
    
    Args:
        db: Database session
        user: The user to assign heroes to
        classes: Dictionary mapping class names to HeroClass instances
    """
    for name, class_name, hp, mp, energy in HERO_SEEDS:
        hero_class = classes[class_name]
        db.add(
            Hero(
                user_id=user.id,
                hero_class_id=hero_class.id,
                name=name,
                hp_current=hp,
                mp_current=mp,
                energy_current=energy,
                attack=hero_class.base_attack,
                defense=hero_class.base_defense,
            )
        )
    
    db.flush()
