from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.missions import count_missions, get_mission, list_missions
from app.ddbb.database import get_db
from app.schemas.mission import MissionRead


class MissionListResponse(BaseModel):
    missions: list[MissionRead]
    page: int
    page_size: int
    total: int


router = APIRouter(tags=["missions"])


@router.get("/missions", response_model=MissionListResponse)
def index(
    page: int = Query(1, ge=1),
    page_size: int = Query(3, ge=1, le=50),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * page_size
    missions = list_missions(db, offset=offset, limit=page_size)
    total = count_missions(db)
    return MissionListResponse(missions=missions, page=page, page_size=page_size, total=total)


@router.get("/missions/{mission_id}", response_model=MissionRead)
def show(mission_id: int, db: Session = Depends(get_db)):
    mission = get_mission(db, mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Misión no encontrada.")
    return mission
