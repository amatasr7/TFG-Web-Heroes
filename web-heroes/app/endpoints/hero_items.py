from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.hero_items import (
    create_hero_item,
    delete_hero_item,
    get_hero_item,
    list_hero_items,
    update_hero_item,
)
from app.ddbb.database import get_db
from app.endpoints.errors import raise_integrity_error
from app.schemas.hero_item import HeroItemCreate, HeroItemRead, HeroItemUpdate

router = APIRouter(tags=["hero-items"])


@router.get("/hero-items", response_model=list[HeroItemRead])
def index(db: Session = Depends(get_db)):
    return list_hero_items(db)


@router.get("/hero-items/{hero_item_id}", response_model=HeroItemRead)
def show(hero_item_id: int, db: Session = Depends(get_db)):
    hero_item = get_hero_item(db, hero_item_id)
    if hero_item is None:
        raise HTTPException(status_code=404, detail="Equipo de heroe no encontrado.")
    return hero_item


@router.post("/hero-items", response_model=HeroItemRead, status_code=status.HTTP_201_CREATED)
def store(payload: HeroItemCreate, db: Session = Depends(get_db)):
    try:
        return create_hero_item(db, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.put("/hero-items/{hero_item_id}", response_model=HeroItemRead)
def replace(hero_item_id: int, payload: HeroItemUpdate, db: Session = Depends(get_db)):
    hero_item = get_hero_item(db, hero_item_id)
    if hero_item is None:
        raise HTTPException(status_code=404, detail="Equipo de heroe no encontrado.")
    try:
        return update_hero_item(db, hero_item, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.patch("/hero-items/{hero_item_id}", response_model=HeroItemRead)
def patch(hero_item_id: int, payload: HeroItemUpdate, db: Session = Depends(get_db)):
    return replace(hero_item_id, payload, db)


@router.delete("/hero-items/{hero_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(hero_item_id: int, db: Session = Depends(get_db)):
    hero_item = get_hero_item(db, hero_item_id)
    if hero_item is None:
        raise HTTPException(status_code=404, detail="Equipo de heroe no encontrado.")
    try:
        delete_hero_item(db, hero_item)
    except IntegrityError as error:
        raise_integrity_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
