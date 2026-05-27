from sqlalchemy.orm import Session, joinedload

from app.crud import base
from app.ddbb.models import Enemy
from app.schemas.enemy import EnemyCreate, EnemyUpdate


def list_enemies(db: Session) -> list[Enemy]:
    return db.query(Enemy).options(joinedload(Enemy.hero_class)).order_by(Enemy.id).all()


def get_enemy(db: Session, enemy_id: int) -> Enemy | None:
    return (
        db.query(Enemy)
        .options(joinedload(Enemy.hero_class))
        .filter(Enemy.id == enemy_id)
        .first()
    )


def create_enemy(db: Session, payload: EnemyCreate) -> Enemy:
    enemy = base.create(db, Enemy, payload)
    return get_enemy(db, enemy.id)


def update_enemy(db: Session, enemy: Enemy, payload: EnemyUpdate) -> Enemy:
    updated = base.update(db, enemy, payload)
    return get_enemy(db, updated.id)


def delete_enemy(db: Session, enemy: Enemy) -> None:
    base.delete(db, enemy)
