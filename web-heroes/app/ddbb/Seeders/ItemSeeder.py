"""Seeder for Item table."""

import random

from sqlalchemy.orm import Session

from app.ddbb.Models import Item
from app.ddbb.Seeders.ItemTypeSeeder import get_or_create_item_type

ITEMS = [
    {"name": "Daga de hierro", "type": "weapon", "sprite_x": 0, "sprite_y": 0, "damage": 1, "hp": 0},
    {"name": "Daga encantada", "type": "weapon", "sprite_x": 0, "sprite_y": 1, "damage": 3, "hp": 0},
    {"name": "Daga bendita", "type": "weapon", "sprite_x": 0, "sprite_y": 2, "damage": 5, "hp": 0},
    {"name": "Daga infernal", "type": "weapon", "sprite_x": 0, "sprite_y": 3, "damage": 7, "hp": 0},
    {"name": "Espada de hierro", "type": "weapon", "sprite_x": 1, "sprite_y": 0, "damage": 2, "hp": 0},
    {"name": "Espada encantada", "type": "weapon", "sprite_x": 1, "sprite_y": 1, "damage": 4, "hp": 0},
    {"name": "Espada bendita", "type": "weapon", "sprite_x": 1, "sprite_y": 2, "damage": 6, "hp": 0},
    {"name": "Espada infernal", "type": "weapon", "sprite_x": 1, "sprite_y": 3, "damage": 8, "hp": 0},
    {"name": "Maza de hierro", "type": "weapon", "sprite_x": 2, "sprite_y": 0, "damage": 2, "hp": 0},
    {"name": "Maza encantada", "type": "weapon", "sprite_x": 2, "sprite_y": 1, "damage": 3, "hp": 0},
    {"name": "Maza bendita", "type": "weapon", "sprite_x": 2, "sprite_y": 2, "damage": 5, "hp": 0},
    {"name": "Maza infernal", "type": "weapon", "sprite_x": 2, "sprite_y": 3, "damage": 7, "hp": 0},
    {"name": "Hacha de hierro", "type": "weapon", "sprite_x": 3, "sprite_y": 0, "damage": 3, "hp": 0},
    {"name": "Hacha encantada", "type": "weapon", "sprite_x": 3, "sprite_y": 1, "damage": 5, "hp": 0},
    {"name": "Hacha bendita", "type": "weapon", "sprite_x": 3, "sprite_y": 2, "damage": 7, "hp": 0},
    {"name": "Hacha infernal", "type": "weapon", "sprite_x": 3, "sprite_y": 3, "damage": 9, "hp": 0},
    {"name": "Lanza de hierro", "type": "weapon", "sprite_x": 4, "sprite_y": 0, "damage": 3, "hp": 0},
    {"name": "Lanza encantada", "type": "weapon", "sprite_x": 4, "sprite_y": 1, "damage": 5, "hp": 0},
    {"name": "Lanza bendita", "type": "weapon", "sprite_x": 4, "sprite_y": 2, "damage": 7, "hp": 0},
    {"name": "Lanza infernal", "type": "weapon", "sprite_x": 4, "sprite_y": 3, "damage": 9, "hp": 0},
    {"name": "Escudo de hierro", "type": "armor", "sprite_x": 5, "sprite_y": 0, "damage": 0, "hp": 2},
    {"name": "Escudo encantado", "type": "armor", "sprite_x": 5, "sprite_y": 1, "damage": 0, "hp": 4},
    {"name": "Escudo bendito", "type": "armor", "sprite_x": 5, "sprite_y": 2, "damage": 0, "hp": 6},
    {"name": "Escudo infernal", "type": "armor", "sprite_x": 5, "sprite_y": 3, "damage": 0, "hp": 8},
    {"name": "Arco de hierro", "type": "weapon", "sprite_x": 6, "sprite_y": 0, "damage": 2, "hp": 0},
    {"name": "Arco encantado", "type": "weapon", "sprite_x": 6, "sprite_y": 1, "damage": 3, "hp": 0},
    {"name": "Arco bendito", "type": "weapon", "sprite_x": 6, "sprite_y": 2, "damage": 5, "hp": 0},
    {"name": "Arco infernal", "type": "weapon", "sprite_x": 6, "sprite_y": 3, "damage": 6, "hp": 0},
    {"name": "Ballesta de hierro", "type": "weapon", "sprite_x": 7, "sprite_y": 0, "damage": 3, "hp": 0},
    {"name": "Ballesta encantada", "type": "weapon", "sprite_x": 7, "sprite_y": 1, "damage": 5, "hp": 0},
    {"name": "Ballesta bendita", "type": "weapon", "sprite_x": 7, "sprite_y": 2, "damage": 7, "hp": 0},
    {"name": "Ballesta infernal", "type": "weapon", "sprite_x": 7, "sprite_y": 3, "damage": 9, "hp": 0},
    {"name": "Armadura de cuero", "type": "armor", "sprite_x": 5, "sprite_y": 6, "damage": 0, "hp": 3},
    {"name": "Armadura de hierro", "type": "armor", "sprite_x": 5, "sprite_y": 7, "damage": 0, "hp": 5},
    {"name": "Armadura de placas", "type": "armor", "sprite_x": 7, "sprite_y": 6, "damage": 0, "hp": 5},
    {"name": "Pocion de Energia", "type": "consumable", "sprite_x": 4, "sprite_y": 0, "damage": 0, "hp": 25},
    {"name": "Pocion de Salud", "type": "consumable", "sprite_x": 5, "sprite_y": 0, "damage": 0, "hp": 25},
    {"name": "Pocion de Mana", "type": "consumable", "sprite_x": 6, "sprite_y": 0, "damage": 0, "mp": 25},
    {"name": "Moneda de oro", "type": "currency", "sprite_x": 7, "sprite_y": 0, "damage": 0, "hp": 0, "value": 1},
    {"name": "Saco de monedas de oro", "type": "currency", "sprite_x": 4, "sprite_y": 5, "damage": 0, "hp": 0, "value_min": 5, "value_max": 20},
    {"name": "Cofre lleno de oro", "type": "container", "sprite_x": 5, "sprite_y": 5, "damage": 0, "hp": 0, "value_min": 10, "value_max": 50},
]


def seed_items(db: Session) -> None:
    """Seed items table."""
    type_cache: dict = {}
    
    for item_data in ITEMS:
        slug = item_data.get("type", "consumable")
        item_type = get_or_create_item_type(db, type_cache, slug)
        
        value = item_data.get("value", 0)
        if "value_min" in item_data and "value_max" in item_data:
            value = random.randint(item_data["value_min"], item_data["value_max"])
        
        db.add(
            Item(
                name=item_data["name"],
                item_type_id=item_type.id,
                sprite_x=item_data.get("sprite_x", 0),
                sprite_y=item_data.get("sprite_y", 0),
                damage_bonus=item_data.get("damage", 0),
                hp_bonus=item_data.get("hp", 0),
                mp_bonus=item_data.get("mp", 0),
                price=item_data.get("price", 0),
                value=value,
            )
        )
    
    db.flush()
