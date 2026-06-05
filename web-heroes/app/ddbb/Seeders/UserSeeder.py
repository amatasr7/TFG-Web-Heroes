from sqlalchemy.orm import Session
from app.ddbb.Models import User
from app.utils.security import hash_password

def seed_users(db: Session) -> User:

    user = User(
        name="Admin",
        email="admin@example.com",
        password=hash_password("admin"),
        is_admin=True,
        gold=50,
    )
    db.add(user)
    db.flush()

    return user
