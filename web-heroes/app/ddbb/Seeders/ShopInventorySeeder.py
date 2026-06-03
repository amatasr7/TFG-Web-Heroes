"""Seeder for shop inventory."""

from sqlalchemy.orm import Session

from app.ddbb.Models import Item, ShopItem


SHOP_ITEMS = [
    # ── Dagas ──
    {"name": "Daga de hierro",    "quantity": 5},
    {"name": "Daga encantada",    "quantity": 4},
    {"name": "Daga bendita",      "quantity": 3},
    {"name": "Daga infernal",     "quantity": 2},
    # ── Espadas ──
    {"name": "Espada de hierro",  "quantity": 5},
    {"name": "Espada encantada",  "quantity": 4},
    {"name": "Espada bendita",    "quantity": 3},
    {"name": "Espada infernal",   "quantity": 2},
    # ── Mazas ──
    {"name": "Maza de hierro",    "quantity": 5},
    {"name": "Maza encantada",    "quantity": 4},
    {"name": "Maza bendita",      "quantity": 3},
    {"name": "Maza infernal",     "quantity": 2},
    # ── Hachas ──
    {"name": "Hacha de hierro",   "quantity": 4},
    {"name": "Hacha encantada",   "quantity": 3},
    {"name": "Hacha bendita",     "quantity": 2},
    {"name": "Hacha infernal",    "quantity": 1},
    # ── Lanzas ──
    {"name": "Lanza de hierro",   "quantity": 4},
    {"name": "Lanza encantada",   "quantity": 3},
    {"name": "Lanza bendita",     "quantity": 2},
    # ── Arcos ──
    {"name": "Arco de hierro",    "quantity": 5},
    {"name": "Arco encantado",    "quantity": 4},
    {"name": "Arco bendito",      "quantity": 3},
    {"name": "Arco infernal",     "quantity": 2},
    # ── Ballestas ──
    {"name": "Ballesta de hierro",  "quantity": 4},
    {"name": "Ballesta encantada",  "quantity": 3},
    {"name": "Ballesta bendita",    "quantity": 2},
    # ── Armaduras ──
    {"name": "Armadura de cuero",   "quantity": 5},
    {"name": "Armadura de hierro",  "quantity": 4},
    {"name": "Armadura de placas",  "quantity": 3},
    # ── Escudos ──
    {"name": "Escudo de hierro",    "quantity": 5},
    {"name": "Escudo encantado",    "quantity": 4},
    {"name": "Escudo bendito",      "quantity": 3},
    {"name": "Escudo infernal",     "quantity": 2},
    # ── Pociones de salud ──
    {"name": "Pocion Menor de Salud",  "quantity": 15},
    {"name": "Pocion de Salud",        "quantity": 12},
    {"name": "Pocion Mayor de Salud",  "quantity": 8},
    {"name": "Elixir de Vida",         "quantity": 4},
    # ── Pociones de maná ──
    {"name": "Pocion Menor de Mana",   "quantity": 15},
    {"name": "Pocion de Mana",         "quantity": 12},
    {"name": "Pocion Mayor de Mana",   "quantity": 8},
    # ── Elixires combinados ──
    {"name": "Elixir Vital",           "quantity": 5},
    {"name": "Pocion de Energia",      "quantity": 10},
    # ── Moneda ──
    {"name": "Saco de monedas de oro", "quantity": 8},
]


def seed_shop_inventory(db: Session) -> None:
    for item_data in SHOP_ITEMS:
        item = db.query(Item).filter(Item.name == item_data["name"]).first()
        if item is None:
            continue

        if db.query(ShopItem).filter(ShopItem.item_id == item.id).first() is None:
            db.add(ShopItem(item_id=item.id, quantity=item_data["quantity"]))

    db.flush()
