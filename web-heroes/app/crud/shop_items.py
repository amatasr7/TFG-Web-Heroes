from sqlalchemy.orm import Session

from app.ddbb.Models import ShopItem


def list_shop_items(db: Session) -> list[ShopItem]:
    return db.query(ShopItem).order_by(ShopItem.id).all()


def get_shop_item(db: Session, item_id: int) -> ShopItem | None:
    return db.query(ShopItem).filter(ShopItem.item_id == item_id).first()


def create_shop_item(db: Session, item_id: int, quantity: int) -> ShopItem:
    shop_item = ShopItem(item_id=item_id, quantity=quantity)
    db.add(shop_item)
    db.commit()
    db.refresh(shop_item)
    return shop_item


def update_shop_item_quantity(db: Session, shop_item: ShopItem, quantity: int) -> ShopItem:
    shop_item.quantity = quantity
    db.commit()
    db.refresh(shop_item)
    return shop_item
