from typing import Any, TypeVar

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.ddbb.database import Base

ModelT = TypeVar("ModelT", bound=Base)


def get(db: Session, model: type[ModelT], item_id: int) -> ModelT | None:
    return db.get(model, item_id)


def list_all(db: Session, model: type[ModelT]) -> list[ModelT]:
    return db.query(model).order_by(model.id).all()


def create(db: Session, model: type[ModelT], payload: BaseModel) -> ModelT:
    data = payload.model_dump(exclude_none=True)
    instance = model(**data)
    db.add(instance)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(instance)
    return instance


def update(db: Session, instance: ModelT, payload: BaseModel) -> ModelT:
    data: dict[str, Any] = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(instance, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(instance)
    return instance


def delete(db: Session, instance: ModelT) -> None:
    db.delete(instance)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
