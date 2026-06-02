from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.warbands import (
    create_warband,
    delete_warband,
    get_warband,
    get_warband_by_user,
    list_warbands,
    update_warband,
)
from app.ddbb.database import get_db
from app.ddbb.Models.Warband import Warband
from app.schemas.warband import WarbandCreate, WarbandRead, WarbandUpdate

router = APIRouter()


def _get_warband_or_404(db: Session, warband_id: int) -> Warband:
    warband = get_warband(db, warband_id)
    if not warband:
        raise HTTPException(status_code=404, detail="Warband not found")
    return warband


@router.get("/warbands", response_model=list[WarbandRead])
def read_warbands(db: Session = Depends(get_db)) -> list[Warband]:
    return list_warbands(db)


@router.get("/warbands/{warband_id}", response_model=WarbandRead)
def read_warband(warband_id: int, db: Session = Depends(get_db)) -> Warband:
    return _get_warband_or_404(db, warband_id)


@router.get("/warbands/user/{user_id}", response_model=WarbandRead)
def read_warband_by_user(user_id: int, db: Session = Depends(get_db)) -> Warband:
    warband = get_warband_by_user(db, user_id)
    if not warband:
        raise HTTPException(status_code=404, detail="Warband not found for user")
    return warband


@router.post("/warbands", response_model=WarbandRead, status_code=201)
def create_warband_endpoint(payload: WarbandCreate, db: Session = Depends(get_db)) -> Warband:
    try:
        return create_warband(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/warbands/{warband_id}", response_model=WarbandRead)
def update_warband_endpoint(
    warband_id: int, payload: WarbandUpdate, db: Session = Depends(get_db)
) -> Warband:
    warband = _get_warband_or_404(db, warband_id)
    try:
        return update_warband(db, warband, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/warbands/{warband_id}", response_model=WarbandRead)
def delete_warband_endpoint(warband_id: int, db: Session = Depends(get_db)) -> Warband:
    warband = _get_warband_or_404(db, warband_id)
    return delete_warband(db, warband)
