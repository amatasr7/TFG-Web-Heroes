import random

from sqlalchemy.orm import Session
from app.ddbb.Models import Item
from app.ddbb.Seeders.ItemTypeSeeder import get_or_create_item_type

ITEMS = [
    # ── Espadas ──
    {"name": "Espada de hierro",  "type": "weapon", "sprite_x": 0, "sprite_y": 1, "damage": 2, "hp": 0, "value": 15},
    {"name": "Espada encantada",  "type": "weapon", "sprite_x": 1, "sprite_y": 1, "damage": 4, "hp": 0, "value": 35},
    {"name": "Espada bendita",    "type": "weapon", "sprite_x": 2, "sprite_y": 1, "damage": 6, "hp": 0, "value": 70},
    {"name": "Espada infernal",   "type": "weapon", "sprite_x": 3, "sprite_y": 1, "damage": 8, "hp": 0, "value": 150},
    # ── Hachas ──
    {"name": "Hacha de hierro",   "type": "weapon", "sprite_x": 0, "sprite_y": 3, "damage": 3, "hp": 0, "value": 20},
    {"name": "Hacha encantada",   "type": "weapon", "sprite_x": 1, "sprite_y": 3, "damage": 5, "hp": 0, "value": 40},
    {"name": "Hacha bendita",     "type": "weapon", "sprite_x": 2, "sprite_y": 3, "damage": 7, "hp": 0, "value": 80},
    {"name": "Hacha infernal",    "type": "weapon", "sprite_x": 3, "sprite_y": 3, "damage": 9, "hp": 0, "value": 160},
    # ── Arcos ──
    {"name": "Arco de hierro",    "type": "weapon", "sprite_x": 0, "sprite_y": 6, "damage": 2, "hp": 0, "value": 15},
    {"name": "Arco encantado",    "type": "weapon", "sprite_x": 1, "sprite_y": 6, "damage": 3, "hp": 0, "value": 25},
    {"name": "Arco bendito",      "type": "weapon", "sprite_x": 2, "sprite_y": 6, "damage": 5, "hp": 0, "value": 50},
    {"name": "Arco infernal",     "type": "weapon", "sprite_x": 3, "sprite_y": 6, "damage": 6, "hp": 0, "value": 100},
    # ── Armaduras ──
    {"name": "Armadura de cuero", "type": "armor",  "sprite_x": 5, "sprite_y": 6, "damage": 0, "hp": 3, "value": 20},
    {"name": "Armadura de hierro","type": "armor",  "sprite_x": 4, "sprite_y": 7, "damage": 0, "hp": 5, "value": 40},
    {"name": "Armadura de placas","type": "armor",  "sprite_x": 5, "sprite_y": 7, "damage": 0, "hp": 7, "value": 70},
    # ── Pociones ──
    {"name": "Pocion de Salud",       "type": "consumable", "sprite_x": 5, "sprite_y": 0, "damage": 0, "hp": 7,  "value": 10},
    {"name": "Pocion de Mana",        "type": "consumable", "sprite_x": 6, "sprite_y": 0, "damage": 0, "mp": 7,  "value": 12},

    {"name": "Contrato de heroe", "type": "consumable", "sprite_x": 4, "sprite_y": 1, "damage": 0, "hp": 0, "value": 200},

    {"name": "Moneda de oro",         "type": "currency",  "sprite_x": 7, "sprite_y": 0, "damage": 0, "hp": 0, "value": 1},
    {"name": "Saco de monedas",       "type": "currency",  "sprite_x": 4, "sprite_y": 5, "damage": 0, "hp": 0, "value_min": 5,  "value_max": 20},
    {"name": "Cofre lleno de oro",    "type": "container", "sprite_x": 5, "sprite_y": 5, "damage": 0, "hp": 0, "value_min": 10, "value_max": 50},
]


def seed_items(db: Session) -> None:
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
