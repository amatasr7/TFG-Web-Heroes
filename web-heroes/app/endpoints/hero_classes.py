from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.hero_classes import (
    create_hero_class,
    delete_hero_class,
    get_hero_class,
    list_hero_classes,
    update_hero_class,
)
from app.ddbb.database import get_db
from app.endpoints.errors import raise_integrity_error
from app.schemas.hero_class import HeroClassCreate, HeroClassRead, HeroClassUpdate

router = APIRouter(tags=["hero-classes"])


@router.get("/hero-classes", response_model=list[HeroClassRead])
def index(db: Session = Depends(get_db)):
    return list_hero_classes(db)


@router.get("/hero-classes/{hero_class_id}", response_model=HeroClassRead)
def show(hero_class_id: int, db: Session = Depends(get_db)):
    hero_class = get_hero_class(db, hero_class_id)
    if hero_class is None:
        raise HTTPException(status_code=404, detail="Clase no encontrada.")
    return hero_class


@router.post("/hero-classes", response_model=HeroClassRead, status_code=status.HTTP_201_CREATED)
def store(payload: HeroClassCreate, db: Session = Depends(get_db)):
    try:
        return create_hero_class(db, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.put("/hero-classes/{hero_class_id}", response_model=HeroClassRead)
def replace(hero_class_id: int, payload: HeroClassUpdate, db: Session = Depends(get_db)):
    hero_class = get_hero_class(db, hero_class_id)
    if hero_class is None:
        raise HTTPException(status_code=404, detail="Clase no encontrada.")
    try:
        return update_hero_class(db, hero_class, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.patch("/hero-classes/{hero_class_id}", response_model=HeroClassRead)
def patch(hero_class_id: int, payload: HeroClassUpdate, db: Session = Depends(get_db)):
    return replace(hero_class_id, payload, db)


@router.delete("/hero-classes/{hero_class_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(hero_class_id: int, db: Session = Depends(get_db)):
    hero_class = get_hero_class(db, hero_class_id)
    if hero_class is None:
        raise HTTPException(status_code=404, detail="Clase no encontrada.")
    try:
        delete_hero_class(db, hero_class)
    except IntegrityError as error:
        raise_integrity_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
