from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.ddbb.Controllers import ShopController
from app.ddbb.database import get_db
from app.schemas.shop_item import ShopItemRead
from app.schemas.user import UserRead
from app.schemas.user_item import UserItemRead

router = APIRouter(tags=["shop"])


class ShopAction(BaseModel):
    user_id: int
    item_id: int
    quantity: int = 1


class UseItemPayload(BaseModel):
    user_id: int
    item_id: int
    hero_id: int


class ShopInventoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: UserRead
    user_items: list[UserItemRead]
    shop_items: list[ShopItemRead]


@router.get("/shop/inventory", response_model=ShopInventoryRead)
def inventory(user_id: int, db: Session = Depends(get_db)):
    try:
        return ShopController.get_inventory(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/shop/buy", response_model=ShopInventoryRead)
def buy(payload: ShopAction, db: Session = Depends(get_db)):
    try:
        return ShopController.buy_item(db, payload.user_id, payload.item_id, payload.quantity)
    except ValueError as e:
        code = 400 if "oro" in str(e).lower() or "unidades" in str(e).lower() or "cantidad" in str(e).lower() else 404
        raise HTTPException(status_code=code, detail=str(e))


@router.post("/shop/sell", response_model=ShopInventoryRead)
def sell(payload: ShopAction, db: Session = Depends(get_db)):
    try:
        return ShopController.sell_item(db, payload.user_id, payload.item_id, payload.quantity)
    except ValueError as e:
        code = 400 if "unidades" in str(e).lower() or "cantidad" in str(e).lower() else 404
        raise HTTPException(status_code=code, detail=str(e))


@router.post("/shop/use-item")
def use_item(payload: UseItemPayload, db: Session = Depends(get_db)):
    try:
        return ShopController.use_item_on_hero(db, payload.user_id, payload.item_id, payload.hero_id)
    except ValueError as e:
        code = 404 if "encontrado" in str(e).lower() else 400
        raise HTTPException(status_code=code, detail=str(e))
