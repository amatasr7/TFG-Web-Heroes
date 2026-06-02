"""Seeder for User table."""

from sqlalchemy.orm import Session

from app.ddbb.Models import User


def seed_users(db: Session) -> User:
    """
    Seed users table.
    
    Returns:
        The created test user instance
    """
    user = User(
        name="Test User",
        email="test@example.com",
        password="",
        is_admin=True,
        gold=50,
    )
    db.add(user)
    db.flush()
    
    return user
