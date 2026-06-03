from sqlalchemy.orm import Session

from app.crud import base
from app.ddbb.Models import Mission
from app.schemas.mission import MissionCreate, MissionUpdate


def list_missions(db: Session, offset: int = 0, limit: int = 3, exclude_ids: list[int] | None = None) -> list[Mission]:
    q = db.query(Mission)
    if exclude_ids:
        q = q.filter(Mission.id.notin_(exclude_ids))
    return q.order_by(Mission.id).offset(offset).limit(limit).all()


def count_missions(db: Session, exclude_ids: list[int] | None = None) -> int:
    q = db.query(Mission)
    if exclude_ids:
        q = q.filter(Mission.id.notin_(exclude_ids))
    return q.count()


def get_mission(db: Session, mission_id: int) -> Mission | None:
    return db.query(Mission).filter(Mission.id == mission_id).first()


def create_mission(db: Session, payload: MissionCreate) -> Mission:
    return base.create(db, Mission, payload)


def update_mission(db: Session, mission: Mission, payload: MissionUpdate) -> Mission:
    return base.update(db, mission, payload)


def delete_mission(db: Session, mission: Mission) -> None:
    base.delete(db, mission)
