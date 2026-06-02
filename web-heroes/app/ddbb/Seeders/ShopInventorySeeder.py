"""Seeder for shop inventory."""

from sqlalchemy.orm import Session

from app.ddbb.Models import Item, ShopItem


SHOP_ITEMS = [
    {"name": "Daga de hierro", "quantity": 6},
    {"name": "Espada encantada", "quantity": 4},
    {"name": "Armadura de hierro", "quantity": 3},
    {"name": "Pocion de Salud", "quantity": 10},
    {"name": "Saco de monedas de oro", "quantity": 5},
]


def seed_shop_inventory(db: Session) -> None:
    for item_data in SHOP_ITEMS:
        item = db.query(Item).filter(Item.name == item_data["name"]).first()
        if item is None:
            continue

        if db.query(ShopItem).filter(ShopItem.item_id == item.id).first() is None:
            db.add(ShopItem(item_id=item.id, quantity=item_data["quantity"]))

    db.flush()
