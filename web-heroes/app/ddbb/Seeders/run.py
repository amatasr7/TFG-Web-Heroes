"""Main seeder runner that orchestrates all database seeders."""

from sqlalchemy.orm import Session

from app.ddbb.Seeders.AbilitySeeder import seed_abilities
from app.ddbb.Seeders.HeroClassSeeder import seed_hero_classes
from app.ddbb.Seeders.ItemSeeder import seed_items
from app.ddbb.Seeders.ItemTypeSeeder import seed_item_types
from app.ddbb.Seeders.UserSeeder import seed_users
from app.ddbb.Seeders.HeroSeeder import seed_heroes
from app.ddbb.Seeders.EnemySeeder import seed_enemies
from app.ddbb.Seeders.MissionSeeder import seed_missions
from app.ddbb.Seeders.ShopInventorySeeder import seed_shop_inventory


def run_all_seeders(db: Session) -> None:
    """
    Run all database seeders in the correct order.

    Execution order respects dependencies between tables:
    1. HeroClass (no dependencies)
    2. ItemType (no dependencies)
    3. User (no dependencies)
    4. Item (depends on ItemType)
    5. Hero (depends on User and HeroClass)
    6. Enemy (depends on HeroClass)
    7. Mission (depends on Enemy)
    8. ShopInventory (depends on Item)

    Args:
        db: Database session
    """
    # Seed base tables (no dependencies)
    seed_abilities(db)
    classes = seed_hero_classes(db)
    seed_item_types(db)
    user = seed_users(db)

    # Seed tables with single-level dependencies
    seed_items(db)
    seed_heroes(db, user, classes)
    enemies = seed_enemies(db, classes)

    # Seed tables with multi-level dependencies
    seed_missions(db, enemies)
    seed_shop_inventory(db)
