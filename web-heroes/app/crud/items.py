from sqlalchemy.orm import Session, joinedload

from app.crud import base
from app.ddbb.Models import Item
from app.schemas.item import ItemCreate, ItemUpdate


def list_items(db: Session) -> list[Item]:
    return db.query(Item).options(joinedload(Item.type)).order_by(Item.id).all()


def get_item(db: Session, item_id: int) -> Item | None:
    return (
        db.query(Item)
        .options(joinedload(Item.type))
        .filter(Item.id == item_id)
        .first()
    )


def create_item(db: Session, payload: ItemCreate) -> Item:
    item = base.create(db, Item, payload)
    return get_item(db, item.id)


def update_item(db: Session, item: Item, payload: ItemUpdate) -> Item:
    updated = base.update(db, item, payload)
    return get_item(db, updated.id)


def delete_item(db: Session, item: Item) -> None:
    base.delete(db, item)
