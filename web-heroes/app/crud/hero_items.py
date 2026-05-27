from sqlalchemy.orm import Session

from app.crud import base
from app.ddbb.models import HeroItem
from app.schemas.hero_item import HeroItemCreate, HeroItemUpdate


def list_hero_items(db: Session) -> list[HeroItem]:
    return db.query(HeroItem).order_by(HeroItem.id).all()


def get_hero_item(db: Session, hero_item_id: int) -> HeroItem | None:
    return db.get(HeroItem, hero_item_id)


def create_hero_item(db: Session, payload: HeroItemCreate) -> HeroItem:
    return base.create(db, HeroItem, payload)


def update_hero_item(db: Session, hero_item: HeroItem, payload: HeroItemUpdate) -> HeroItem:
    return base.update(db, hero_item, payload)


def delete_hero_item(db: Session, hero_item: HeroItem) -> None:
    base.delete(db, hero_item)
