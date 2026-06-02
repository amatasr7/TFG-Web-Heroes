"""Database seeding orchestrator."""

from app.ddbb.database import SessionLocal
from app.ddbb.Models import HeroClass
from app.ddbb.Seeders import run_all_seeders


def seed_database() -> None:
    """
    Seed the database with initial data.
    
    This function checks if data already exists and only seeds if the database is empty.
    It delegates the actual seeding to individual seeders in the Seeders module.
    """
    db = SessionLocal()
    try:
        if db.query(HeroClass).first():
            return

        run_all_seeders(db)
        db.commit()
    finally:
        db.close()
