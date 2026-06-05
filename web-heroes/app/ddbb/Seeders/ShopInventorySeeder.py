"""Seeder for shop inventory."""

from sqlalchemy.orm import Session

from app.ddbb.Models import Item, ShopItem


SHOP_ITEMS = [

    # ── Espadas ──
    {"name": "Espada de hierro",  "quantity": 5},
    {"name": "Espada encantada",  "quantity": 4},
    {"name": "Espada bendita",    "quantity": 3},
    {"name": "Espada infernal",   "quantity": 2},

    # ── Hachas ──
    {"name": "Hacha de hierro",   "quantity": 4},
    {"name": "Hacha encantada",   "quantity": 3},
    {"name": "Hacha bendita",     "quantity": 2},
    {"name": "Hacha infernal",    "quantity": 1},

    # ── Arcos ──
    {"name": "Arco de hierro",    "quantity": 5},
    {"name": "Arco encantado",    "quantity": 4},
    {"name": "Arco bendito",      "quantity": 3},
    {"name": "Arco infernal",     "quantity": 2},
    # ── Armaduras ──
    {"name": "Armadura de cuero",   "quantity": 5},
    {"name": "Armadura de hierro",  "quantity": 4},
    {"name": "Armadura de placas",  "quantity": 3},
    # ── Pociones ──
    {"name": "Pocion de Salud",        "quantity": 12},
    {"name": "Pocion de Mana",         "quantity": 12},
    # ── Otros ──
    {"name": "Contrato de heroe",       "quantity": 5},
]


def seed_shop_inventory(db: Session) -> None:
    for item_data in SHOP_ITEMS:
        item = db.query(Item).filter(Item.name == item_data["name"]).first()
        if item is None:
            continue

        if db.query(ShopItem).filter(ShopItem.item_id == item.id).first() is None:
            db.add(ShopItem(item_id=item.id, quantity=item_data["quantity"]))

    db.flush()
