from sqlalchemy.orm import Session

from app.crud import base
from app.ddbb.Models import HeroClass
from app.schemas.hero_class import HeroClassCreate, HeroClassUpdate


def list_hero_classes(db: Session) -> list[HeroClass]:
    return db.query(HeroClass).order_by(HeroClass.id).all()


def get_hero_class(db: Session, hero_class_id: int) -> HeroClass | None:
    return db.get(HeroClass, hero_class_id)


def create_hero_class(db: Session, payload: HeroClassCreate) -> HeroClass:
    return base.create(db, HeroClass, payload)


def update_hero_class(db: Session, hero_class: HeroClass, payload: HeroClassUpdate) -> HeroClass:
    return base.update(db, hero_class, payload)


def delete_hero_class(db: Session, hero_class: HeroClass) -> None:
    base.delete(db, hero_class)
