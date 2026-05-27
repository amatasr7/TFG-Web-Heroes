from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.items import create_item, delete_item, get_item, list_items, update_item
from app.ddbb.database import get_db
from app.endpoints.errors import raise_integrity_error
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter(tags=["items"])


@router.get("/items", response_model=list[ItemRead])
def index(db: Session = Depends(get_db)):
    return list_items(db)


@router.get("/items/{item_id}", response_model=ItemRead)
def show(item_id: int, db: Session = Depends(get_db)):
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado.")
    return item


@router.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def store(payload: ItemCreate, db: Session = Depends(get_db)):
    try:
        return create_item(db, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.put("/items/{item_id}", response_model=ItemRead)
def replace(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado.")
    try:
        return update_item(db, item, payload)
    except IntegrityError as error:
        raise_integrity_error(error)


@router.patch("/items/{item_id}", response_model=ItemRead)
def patch(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    return replace(item_id, payload, db)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(item_id: int, db: Session = Depends(get_db)):
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado.")
    try:
        delete_item(db, item)
    except IntegrityError as error:
        raise_integrity_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
