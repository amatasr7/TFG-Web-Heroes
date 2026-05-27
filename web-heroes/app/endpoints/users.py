from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.users import create_user, delete_user, get_user, list_users, update_user
from app.ddbb.database import get_db
from app.endpoints.errors import raise_integrity_error
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(tags=["users"])


@router.get("/users", response_model=list[UserRead])
def index(db: Session = Depends(get_db)):
    return list_users(db)


@router.get("/users/{user_id}", response_model=UserRead)
def show(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def store(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.put("/users/{user_id}", response_model=UserRead)
def replace(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    try:
        return update_user(db, user, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.patch("/users/{user_id}", response_model=UserRead)
def patch(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return replace(user_id, payload, db)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    try:
        delete_user(db, user)
    except IntegrityError as error:
        raise_integrity_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
