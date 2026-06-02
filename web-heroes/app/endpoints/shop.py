from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.crud.items import get_item
from app.crud.shop_items import create_shop_item, get_shop_item, list_shop_items, update_shop_item_quantity
from app.crud.user_items import create_user_item, get_user_item, list_user_items, update_user_item_quantity
from app.crud.users import get_user
from app.ddbb.Models import ShopItem, UserItem
from app.ddbb.database import get_db
from app.schemas.shop_item import ShopItemRead
from app.schemas.user import UserRead
from app.schemas.user_item import UserItemRead

router = APIRouter(tags=["shop"])


class ShopAction(BaseModel):
    user_id: int
    item_id: int
    quantity: int = 1


class ShopInventoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: UserRead
    user_items: list[UserItemRead]
    shop_items: list[ShopItemRead]


@router.get("/shop/inventory", response_model=ShopInventoryRead)
def inventory(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    return {
        "user": user,
        "user_items": list_user_items(db, user_id),
        "shop_items": list_shop_items(db),
    }


@router.post("/shop/buy", response_model=ShopInventoryRead)
def buy(payload: ShopAction, db: Session = Depends(get_db)):
    if payload.quantity <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor que cero.")

    user = get_user(db, payload.user_id)
    item = get_item(db, payload.item_id)
    shop_item = get_shop_item(db, payload.item_id)

    if user is None or item is None or shop_item is None:
        raise HTTPException(status_code=404, detail="Usuario, item o inventario de tienda no encontrado.")

    total_price = item.value * payload.quantity
    if shop_item.quantity < payload.quantity:
        raise HTTPException(status_code=400, detail="No hay suficientes unidades en el inventario del vendedor.")
    if user.gold < total_price:
        raise HTTPException(status_code=400, detail="No tienes suficiente oro para comprar este item.")

    user.gold -= total_price
    shop_item.quantity -= payload.quantity
    update_shop_item_quantity(db, shop_item, shop_item.quantity)

    user_item = get_user_item(db, user.id, item.id)
    if user_item is None:
        create_user_item(db, user.id, item.id, payload.quantity)
    else:
        update_user_item_quantity(db, user_item, user_item.quantity + payload.quantity)

    db.commit()
    db.refresh(user)

    return {
        "user": user,
        "user_items": list_user_items(db, user.id),
        "shop_items": list_shop_items(db),
    }


@router.post("/shop/sell", response_model=ShopInventoryRead)
def sell(payload: ShopAction, db: Session = Depends(get_db)):
    if payload.quantity <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor que cero.")

    user = get_user(db, payload.user_id)
    item = get_item(db, payload.item_id)
    if user is None or item is None:
        raise HTTPException(status_code=404, detail="Usuario o item no encontrado.")

    user_item = get_user_item(db, user.id, item.id)
    if user_item is None or user_item.quantity < payload.quantity:
        raise HTTPException(status_code=400, detail="No tienes suficientes unidades de ese item para vender.")

    total_price = item.value * payload.quantity
    user.gold += total_price

    remaining_quantity = user_item.quantity - payload.quantity
    update_user_item_quantity(db, user_item, remaining_quantity)

    shop_item = get_shop_item(db, item.id)
    if shop_item is None:
        create_shop_item(db, item.id, payload.quantity)
    else:
        update_shop_item_quantity(db, shop_item, shop_item.quantity + payload.quantity)

    db.commit()
    db.refresh(user)

    return {
        "user": user,
        "user_items": list_user_items(db, user.id),
        "shop_items": list_shop_items(db),
    }
