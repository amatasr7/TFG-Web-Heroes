from sqlalchemy.orm import Session

from app.crud import base
from app.ddbb.models import User
from app.schemas.user import UserCreate, UserUpdate


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id).all()


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def create_user(db: Session, payload: UserCreate) -> User:
    return base.create(db, User, payload)


def update_user(db: Session, user: User, payload: UserUpdate) -> User:
    return base.update(db, user, payload)


def delete_user(db: Session, user: User) -> None:
    base.delete(db, user)
