"""Database seeding orchestrator."""

from app.ddbb.database import SessionLocal
from app.ddbb.Models import HeroClass, ShopItem
from app.ddbb.Models.Ability import Ability
from app.ddbb.Seeders import run_all_seeders
from app.ddbb.Seeders.AbilitySeeder import seed_abilities
from app.ddbb.Seeders.ShopInventorySeeder import seed_shop_inventory


def seed_database() -> None:
    """
    Seed the database with initial data.

    Full seeding only runs on an empty database (no HeroClass rows).
    Shop inventory and abilities are seeded independently so they populate on
    existing databases after new tables are added.
    """
    db = SessionLocal()
    try:
        if db.query(HeroClass).first():
            # DB already seeded — backfill any new tables if empty
            if not db.query(ShopItem).first():
                seed_shop_inventory(db)
                db.commit()
            if not db.query(Ability).first():
                seed_abilities(db)
                db.commit()
            return

        run_all_seeders(db)
        db.commit()
    finally:
        db.close()
