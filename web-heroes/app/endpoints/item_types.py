from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.item_types import create_item_type, delete_item_type, get_item_type, list_item_types, update_item_type
from app.ddbb.database import get_db
from app.endpoints.errors import raise_integrity_error
from app.schemas.item_type import ItemTypeCreate, ItemTypeRead, ItemTypeUpdate

router = APIRouter(tags=["item-types"])


@router.get("/item-types", response_model=list[ItemTypeRead])
def index(db: Session = Depends(get_db)):
    return list_item_types(db)


@router.get("/item-types/{item_type_id}", response_model=ItemTypeRead)
def show(item_type_id: int, db: Session = Depends(get_db)):
    item_type = get_item_type(db, item_type_id)
    if item_type is None:
        raise HTTPException(status_code=404, detail="Tipo de item no encontrado.")
    return item_type


@router.post("/item-types", response_model=ItemTypeRead, status_code=status.HTTP_201_CREATED)
def store(payload: ItemTypeCreate, db: Session = Depends(get_db)):
    try:
        return create_item_type(db, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.put("/item-types/{item_type_id}", response_model=ItemTypeRead)
def replace(item_type_id: int, payload: ItemTypeUpdate, db: Session = Depends(get_db)):
    item_type = get_item_type(db, item_type_id)
    if item_type is None:
        raise HTTPException(status_code=404, detail="Tipo de item no encontrado.")
    try:
        return update_item_type(db, item_type, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.patch("/item-types/{item_type_id}", response_model=ItemTypeRead)
def patch(item_type_id: int, payload: ItemTypeUpdate, db: Session = Depends(get_db)):
    return replace(item_type_id, payload, db)


@router.delete("/item-types/{item_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(item_type_id: int, db: Session = Depends(get_db)):
    item_type = get_item_type(db, item_type_id)
    if item_type is None:
        raise HTTPException(status_code=404, detail="Tipo de item no encontrado.")
    try:
        delete_item_type(db, item_type)
    except IntegrityError as error:
        raise_integrity_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
