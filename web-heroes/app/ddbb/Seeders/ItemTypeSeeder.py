"""Seeder for ItemType table."""

from sqlalchemy.orm import Session

from app.ddbb.Models import ItemType


def seed_item_types(db: Session) -> dict[str, ItemType]:
    """
    Seed item types table.
    
    Creates item types on demand from items, so this function
    just returns an empty cache to be populated during item seeding.
    
    Returns:
        An empty dictionary to be populated during item seeding
    """
    # Item types are created on-demand during item seeding
    return {}


def get_or_create_item_type(db: Session, type_cache: dict[str, ItemType], slug: str) -> ItemType:
    """
    Get or create an item type by slug.
    
    Args:
        db: Database session
        type_cache: Cache dictionary for item types
        slug: The slug identifier for the item type
        
    Returns:
        The ItemType instance
    """
    if slug not in type_cache:
        item_type = ItemType(name=slug.capitalize(), slug=slug)
        db.add(item_type)
        db.flush()
        type_cache[slug] = item_type
    
    return type_cache[slug]
