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


@router.post("/shop/use-item")
def use_item(payload: UseItemPayload, db: Session = Depends(get_db)):
    """Use one consumable item on a hero, restoring HP and/or MP."""
    from app.crud.heroes import get_hero

    user_item = get_user_item(db, payload.user_id, payload.item_id)
    if not user_item or user_item.quantity <= 0:
        raise HTTPException(status_code=400, detail="No tienes este objeto.")

    item = get_item(db, payload.item_id)
    if item is None or item.type.slug != "consumable":
        raise HTTPException(status_code=400, detail="Este objeto no es consumible.")

    hero = get_hero(db, payload.hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Héroe no encontrado.")

    max_hp = hero.hero_class.base_hp_max
    max_mp = hero.hero_class.base_mp_max
    hp_restored = min(item.hp_bonus, max_hp - hero.hp_current)
    mp_restored = min(item.mp_bonus, max_mp - hero.mp_current)

    hero.hp_current = min(max_hp, hero.hp_current + item.hp_bonus)
    hero.mp_current = min(max_mp, hero.mp_current + item.mp_bonus)

    new_qty = user_item.quantity - 1
    update_user_item_quantity(db, user_item, new_qty)

    db.commit()
    db.refresh(hero)

    return {
        "hp_restored": hp_restored,
        "mp_restored": mp_restored,
        "item_name": item.name,
        "quantity_remaining": new_qty,
        "hero_id": hero.id,
        "hero_hp": hero.hp_current,
        "hero_mp": hero.mp_current,
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
