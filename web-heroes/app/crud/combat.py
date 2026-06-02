import random

from sqlalchemy.orm import Session

from app.crud.heroes import add_experience
from app.ddbb.Models import Enemy, Hero


def calculate_damage(attacker: Hero) -> int:
    return 3 if attacker.hero_class.name == "Guerrero" else 2


def handle_hero_attack(db: Session, hero: Hero, enemy: Enemy) -> dict:
    combat_log: list[str] = []

    if random.randint(1, 100) <= 80:
        damage_to_enemy = calculate_damage(hero)
        enemy.hp_current -= damage_to_enemy
        combat_log.append(f"{hero.name} ataca a {enemy.name}.")
    else:
        combat_log.append(f"{hero.name} intenta atacar, pero {enemy.name} esquiva el golpe.")

    if enemy.hp_current > 0:
        if random.randint(1, 100) <= 60:
            hero.hp_current -= 1
            combat_log.append(f"{enemy.name} ataca a {hero.name}.")
        else:
            combat_log.append(f"{enemy.name} intenta contraatacar a {hero.name}, pero falla.")

    rewards = None
    if enemy.hp_current <= 0:
        enemy.hp_current = 0
        db.commit()
        rewards = add_experience(db, hero, enemy.xp_reward)
        combat_log.append(f"El grupo ha derrotado a {enemy.name}!")
    else:
        db.commit()

    db.refresh(hero)
    db.refresh(enemy)

    return {
        "combat_log": combat_log,
        "hero_status": {
            "hp_remaining": hero.hp_current,
            "is_dead": hero.hp_current <= 0,
        },
        "enemy_status": {
            "hp_remaining": enemy.hp_current,
            "is_dead": enemy.hp_current <= 0,
        },
        "rewards": rewards,
    }
