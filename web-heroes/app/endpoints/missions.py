from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.ddbb.Controllers import MissionController
from app.ddbb.database import get_db
from app.schemas.mission import MissionRead


class MissionListResponse(BaseModel):
    missions: list[MissionRead]
    page: int
    page_size: int
    total: int
    guild_rank: int = 0


class MissionCompletePayload(BaseModel):
    user_id: int
    hero_ids: list[int]


router = APIRouter(tags=["missions"])


@router.get("/missions", response_model=MissionListResponse)
def index(
    page: int = Query(1, ge=1),
    page_size: int = Query(3, ge=1, le=50),
    user_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    result = MissionController.get_available_missions(db, user_id, page, page_size)
    return MissionListResponse(**result)


@router.get("/missions/{mission_id}", response_model=MissionRead)
def show(mission_id: int, db: Session = Depends(get_db)):
    mission = MissionController.get_mission_by_id(db, mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Misión no encontrada.")
    return mission


@router.post("/missions/{mission_id}/complete")
def complete_mission(mission_id: int, payload: MissionCompletePayload, db: Session = Depends(get_db)):
    try:
        return MissionController.complete_mission(db, mission_id, payload.user_id, payload.hero_ids)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
