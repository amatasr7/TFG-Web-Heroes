from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.heroes import create_hero, delete_hero, get_hero, list_heroes, refresh_hero_stats, update_hero
from app.ddbb.database import get_db
from app.endpoints.errors import raise_integrity_error
from app.schemas.hero import HeroCreate, HeroRead, HeroUpdate

router = APIRouter(tags=["heroes"])


@router.get("/heroes", response_model=list[HeroRead])
def index(db: Session = Depends(get_db)):
    return list_heroes(db)


@router.get("/heroes/{hero_id}", response_model=HeroRead)
def show(hero_id: int, db: Session = Depends(get_db)):
    hero = get_hero(db, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado.")
    return refresh_hero_stats(db, hero)


@router.post("/heroes", response_model=HeroRead, status_code=status.HTTP_201_CREATED)
def store(payload: HeroCreate, db: Session = Depends(get_db)):
    try:
        return create_hero(db, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.put("/heroes/{hero_id}", response_model=HeroRead)
def replace(hero_id: int, payload: HeroUpdate, db: Session = Depends(get_db)):
    hero = get_hero(db, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado.")
    try:
        return update_hero(db, hero, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.patch("/heroes/{hero_id}", response_model=HeroRead)
def patch(hero_id: int, payload: HeroUpdate, db: Session = Depends(get_db)):
    return replace(hero_id, payload, db)


@router.delete("/heroes/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(hero_id: int, db: Session = Depends(get_db)):
    hero = get_hero(db, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado.")
    try:
        delete_hero(db, hero)
    except IntegrityError as error:
        raise_integrity_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
