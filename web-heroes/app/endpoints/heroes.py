from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.heroes import get_hero
from app.ddbb.Controllers import HeroController
from app.ddbb.Controllers.HeroController import CreateWithContractPayload
from app.ddbb.database import get_db
from app.endpoints.errors import or_404, raise_integrity_error
from app.schemas.hero import HeroCreate, HeroRead, HeroUpdate

router = APIRouter(tags=["heroes"])


class LevelUpPayload(BaseModel):
    stat: str  # "hp" | "mp" | "attack" | "defense"


class ActionPayload(BaseModel):
    action: str   # "meditate" | "train" | "steal"
    user_id: int | None = None


@router.post("/heroes/create-with-contract", response_model=HeroRead, status_code=status.HTTP_201_CREATED)
def create_with_contract(payload: CreateWithContractPayload, db: Session = Depends(get_db)):
    try:
        return HeroController.create_hero_with_contract(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/heroes", response_model=list[HeroRead])
def index(user_id: int | None = None, db: Session = Depends(get_db)):
    return HeroController.get_heroes_for_user(db, user_id)


@router.get("/heroes/{hero_id}", response_model=HeroRead)
def show(hero_id: int, db: Session = Depends(get_db)):
    return or_404(HeroController.get_hero_with_refresh(db, hero_id), "Heroe no encontrado.")


@router.post("/heroes", response_model=HeroRead, status_code=status.HTTP_201_CREATED)
def store(payload: HeroCreate, db: Session = Depends(get_db)):
    try:
        return HeroController.create_new_hero(db, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.put("/heroes/{hero_id}", response_model=HeroRead)
def replace(hero_id: int, payload: HeroUpdate, db: Session = Depends(get_db)):
    hero = or_404(get_hero(db, hero_id), "Heroe no encontrado.")
    try:
        return HeroController.update_hero_data(db, hero, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.patch("/heroes/{hero_id}", response_model=HeroRead)
def patch(hero_id: int, payload: HeroUpdate, db: Session = Depends(get_db)):
    return replace(hero_id, payload, db)


@router.delete("/heroes/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(hero_id: int, db: Session = Depends(get_db)):
    hero = or_404(get_hero(db, hero_id), "Heroe no encontrado.")
    try:
        HeroController.delete_hero_record(db, hero)
    except IntegrityError as error:
        raise_integrity_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/heroes/{hero_id}/rest", response_model=HeroRead)
def rest(hero_id: int, db: Session = Depends(get_db)):
    hero = or_404(get_hero(db, hero_id), "Heroe no encontrado.")
    return HeroController.rest_hero_energy(db, hero)


@router.post("/heroes/{hero_id}/level-up", response_model=HeroRead)
def level_up(hero_id: int, payload: LevelUpPayload, db: Session = Depends(get_db)):
    hero = or_404(get_hero(db, hero_id), "Heroe no encontrado.")
    try:
        return HeroController.level_up(db, hero, payload.stat)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/heroes/{hero_id}/action")
def class_action(hero_id: int, payload: ActionPayload, db: Session = Depends(get_db)):
    hero = or_404(get_hero(db, hero_id), "Heroe no encontrado.")
    try:
        return HeroController.execute_class_action(db, hero, payload.action, payload.user_id)
    except ValueError as e:
        status_code = 429 if "recarga" in str(e).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(e))
