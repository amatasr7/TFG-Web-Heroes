from sqlalchemy.orm import Session

from app.ddbb.Models.UserMission import UserMission


def get_completed_mission_ids(db: Session, user_id: int) -> list[int]:
    rows = db.query(UserMission.mission_id).filter(UserMission.user_id == user_id).all()
    return [r[0] for r in rows]


def count_completed_missions(db: Session, user_id: int) -> int:
    return db.query(UserMission).filter(UserMission.user_id == user_id).count()


def mark_mission_completed(db: Session, user_id: int, mission_id: int) -> UserMission:
    existing = (
        db.query(UserMission)
        .filter(UserMission.user_id == user_id, UserMission.mission_id == mission_id)
        .first()
    )
    if existing:
        return existing
    record = UserMission(user_id=user_id, mission_id=mission_id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
