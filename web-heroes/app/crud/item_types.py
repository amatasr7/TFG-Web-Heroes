from sqlalchemy.orm import Session

from app.crud import base
from app.ddbb.Models import ItemType
from app.schemas.item_type import ItemTypeCreate, ItemTypeUpdate


def list_item_types(db: Session) -> list[ItemType]:
    return db.query(ItemType).order_by(ItemType.id).all()


def get_item_type(db: Session, item_type_id: int) -> ItemType | None:
    return db.get(ItemType, item_type_id)


def create_item_type(db: Session, payload: ItemTypeCreate) -> ItemType:
    return base.create(db, ItemType, payload)


def update_item_type(db: Session, item_type: ItemType, payload: ItemTypeUpdate) -> ItemType:
    return base.update(db, item_type, payload)


def delete_item_type(db: Session, item_type: ItemType) -> None:
    base.delete(db, item_type)
