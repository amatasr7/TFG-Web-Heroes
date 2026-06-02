"""Database seeding orchestrator."""

from app.ddbb.database import SessionLocal
from app.ddbb.Models import HeroClass, ShopItem
from app.ddbb.Seeders import run_all_seeders
from app.ddbb.Seeders.ShopInventorySeeder import seed_shop_inventory


def seed_database() -> None:
    """
    Seed the database with initial data.

    Full seeding only runs on an empty database (no HeroClass rows).
    Shop inventory is seeded independently so it also populates on existing databases
    after the migration adds the shop_items table.
    """
    db = SessionLocal()
    try:
        if db.query(HeroClass).first():
            # DB already seeded — only fill shop inventory if it is empty
            if not db.query(ShopItem).first():
                seed_shop_inventory(db)
                db.commit()
            return

        run_all_seeders(db)
        db.commit()
    finally:
        db.close()
