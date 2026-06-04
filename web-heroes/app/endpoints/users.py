from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.ddbb.Controllers import UserController
from app.ddbb.database import get_db
from app.endpoints.errors import raise_integrity_error
from app.schemas.user import UserCreate, UserLogin, UserRead, UserUpdate

router = APIRouter(tags=["users"])


@router.get("/users", response_model=list[UserRead])
def index(db: Session = Depends(get_db)):
    return UserController.list_all_users(db)


@router.get("/users/{user_id}", response_model=UserRead)
def show(user_id: int, db: Session = Depends(get_db)):
    user = UserController.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def store(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserController.register_user(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError as error:
        raise_integrity_error(error)


@router.post("/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserController.register_user(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError as error:
        raise_integrity_error(error)


@router.post("/auth/login", response_model=UserRead)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    try:
        return UserController.login_user(db, payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.put("/users/{user_id}", response_model=UserRead)
def replace(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = UserController.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    try:
        return UserController.update_user_data(db, user, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.patch("/users/{user_id}", response_model=UserRead)
def patch(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return replace(user_id, payload, db)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(user_id: int, db: Session = Depends(get_db)):
    user = UserController.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    try:
        UserController.delete_user_account(db, user)
    except IntegrityError as error:
        raise_integrity_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
