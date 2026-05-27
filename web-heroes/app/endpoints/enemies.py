from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.enemies import create_enemy, delete_enemy, get_enemy, list_enemies, update_enemy
from app.ddbb.database import get_db
from app.endpoints.errors import raise_integrity_error
from app.schemas.enemy import EnemyCreate, EnemyRead, EnemyUpdate

router = APIRouter(tags=["enemies"])


@router.get("/enemies", response_model=list[EnemyRead])
def index(db: Session = Depends(get_db)):
    return list_enemies(db)


@router.get("/enemies/{enemy_id}", response_model=EnemyRead)
def show(enemy_id: int, db: Session = Depends(get_db)):
    enemy = get_enemy(db, enemy_id)
    if enemy is None:
        raise HTTPException(status_code=404, detail="Enemigo no encontrado.")
    return enemy


@router.post("/enemies", response_model=EnemyRead, status_code=status.HTTP_201_CREATED)
def store(payload: EnemyCreate, db: Session = Depends(get_db)):
    try:
        return create_enemy(db, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.put("/enemies/{enemy_id}", response_model=EnemyRead)
def replace(enemy_id: int, payload: EnemyUpdate, db: Session = Depends(get_db)):
    enemy = get_enemy(db, enemy_id)
    if enemy is None:
        raise HTTPException(status_code=404, detail="Enemigo no encontrado.")
    try:
        return update_enemy(db, enemy, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.patch("/enemies/{enemy_id}", response_model=EnemyRead)
def patch(enemy_id: int, payload: EnemyUpdate, db: Session = Depends(get_db)):
    return replace(enemy_id, payload, db)


@router.delete("/enemies/{enemy_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(enemy_id: int, db: Session = Depends(get_db)):
    enemy = get_enemy(db, enemy_id)
    if enemy is None:
        raise HTTPException(status_code=404, detail="Enemigo no encontrado.")
    try:
        delete_enemy(db, enemy)
    except IntegrityError as error:
        raise_integrity_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
