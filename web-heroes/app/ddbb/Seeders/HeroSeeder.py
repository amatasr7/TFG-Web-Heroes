from sqlalchemy.orm import Session
from app.ddbb.Models import Hero, HeroClass, User
from app.crud.heroes import equip_starting_items

HERO_SEEDS = [
    ("Varian", "Guerrero", 10, 2, 10),
    ("Sharyn", "Mago", 6, 10, 10),
    ("Deloth", "Picaro", 8, 5, 10),
]

def seed_heroes(db: Session, user: User, classes: dict[str, HeroClass]) -> None:

    for name, class_name, hp, mp, energy in HERO_SEEDS:
        hero_class = classes[class_name]
        hero = Hero(
            user_id=user.id,
            hero_class_id=hero_class.id,
            name=name,
            hp_current=hp,
            mp_current=mp,
            energy_current=energy,
            attack=hero_class.base_attack,
            defense=hero_class.base_defense,
        )
        hero.hero_class = hero_class
        db.add(hero)
        db.flush()
        equip_starting_items(db, hero)

    db.flush()
