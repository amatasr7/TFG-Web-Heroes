from sqlalchemy.orm import Session

from app.crud import base
from app.ddbb.Models import Hero, HeroClass, User
from app.crud.warbands import create_warband_for_user
from app.schemas.user import UserCreate, UserLogin, UserUpdate
from app.utils.security import hash_password, verify_password


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id).all()


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, payload: UserCreate) -> User:
    hashed_password = hash_password(payload.password)
    user_data = payload.model_dump(exclude_none=True, exclude={"password"})
    user = User(**user_data, password=hashed_password)
    db.add(user)
    db.flush()

    starter_heroes = [
        ("Aragorn", "Guerrero", 10, 2, 10),
        ("Morgana", "Mago", 6, 10, 10),
        ("Sombra", "Picaro", 8, 5, 10),
    ]

    hero_classes = db.query(HeroClass).filter(HeroClass.name.in_([c for _, c, *_ in starter_heroes])).all()
    hero_class_map = {hero_class.name: hero_class for hero_class in hero_classes}

    if len(hero_class_map) != len(starter_heroes):
        raise ValueError("Hero classes for the starter warband are missing.")

    created_heroes: list[Hero] = []
    for name, class_name, hp, mp, energy in starter_heroes:
        hero_class = hero_class_map[class_name]
        hero = Hero(
            user_id=user.id,
            hero_class_id=hero_class.id,
            name=name,
            hp_current=hp,
            mp_current=mp,
            energy_current=energy,
            attack=hero_class.base_attack,
            defense=hero_class.base_defense,
        )
        db.add(hero)
        created_heroes.append(hero)

    db.flush()
    hero_ids = [hero.id for hero in created_heroes]
    create_warband_for_user(db, user.id, hero_ids, name=f"{user.name} Warband")
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user is None:
        return None
    return user if verify_password(password, user.password) else None


def update_user(db: Session, user: User, payload: UserUpdate) -> User:
    return base.update(db, user, payload)


def delete_user(db: Session, user: User) -> None:
    base.delete(db, user)
