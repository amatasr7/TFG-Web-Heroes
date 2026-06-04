"""User business logic: authentication and account management."""
from sqlalchemy.orm import Session

from app.crud.users import (
    authenticate_user,
    create_user,
    delete_user,
    get_user,
    get_user_by_email,
    list_users,
    update_user,
)
from app.ddbb.Models import User
from app.schemas.user import UserCreate, UserUpdate


def list_all_users(db: Session) -> list[User]:
    return list_users(db)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return get_user(db, user_id)


def register_user(db: Session, payload: UserCreate) -> User:
    if get_user_by_email(db, payload.email) is not None:
        raise ValueError("El correo electrónico ya está registrado.")
    return create_user(db, payload)


def login_user(db: Session, email: str, password: str) -> User:
    user = authenticate_user(db, email, password)
    if user is None:
        raise ValueError("Correo o contraseña incorrectos.")
    return user


def update_user_data(db: Session, user: User, payload: UserUpdate) -> User:
    return update_user(db, user, payload)


def delete_user_account(db: Session, user: User) -> None:
    delete_user(db, user)
