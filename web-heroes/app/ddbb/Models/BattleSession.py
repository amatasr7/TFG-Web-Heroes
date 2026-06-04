from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.ddbb.database import Base


class BattleSession(Base):
    __tablename__ = "battle_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    mission_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("missions.id"), nullable=True)
    turn_queue: Mapped[list] = mapped_column(JSON, default=list)
    current_turn_index: Mapped[int] = mapped_column(Integer, default=0)
    heroes_state: Mapped[list] = mapped_column(JSON, default=list)
    enemies_state: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(20), default="active")  # active|victory|defeat|abandoned
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
