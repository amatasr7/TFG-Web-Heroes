"""Shop business logic: buy/sell validation, consumable use."""
from sqlalchemy.orm import Session

from app.crud.items import get_item
from app.crud.shop_items import create_shop_item, get_shop_item, list_shop_items, update_shop_item_quantity
from app.crud.user_items import create_user_item, get_user_item, list_user_items, update_user_item_quantity
from app.crud.users import get_user


def get_inventory(db: Session, user_id: int) -> dict:
    user = get_user(db, user_id)
    if user is None:
        raise ValueError("Usuario no encontrado.")
    return {
        "user": user,
        "user_items": list_user_items(db, user_id),
        "shop_items": list_shop_items(db),
    }


def buy_item(db: Session, user_id: int, item_id: int, quantity: int) -> dict:
    if quantity <= 0:
        raise ValueError("La cantidad debe ser mayor que cero.")

    user = get_user(db, user_id)
    item = get_item(db, item_id)
    shop_item = get_shop_item(db, item_id)

    if user is None or item is None or shop_item is None:
        raise ValueError("Usuario, item o inventario de tienda no encontrado.")

    total_price = item.value * quantity
    if shop_item.quantity < quantity:
        raise ValueError("No hay suficientes unidades en el inventario del vendedor.")
    if user.gold < total_price:
        raise ValueError("No tienes suficiente oro para comprar este item.")

    user.gold -= total_price
    shop_item.quantity -= quantity
    update_shop_item_quantity(db, shop_item, shop_item.quantity)

    user_item = get_user_item(db, user_id, item_id)
    if user_item is None:
        create_user_item(db, user_id, item_id, quantity)
    else:
        update_user_item_quantity(db, user_item, user_item.quantity + quantity)

    db.commit()
    db.refresh(user)

    return {
        "user": user,
        "user_items": list_user_items(db, user_id),
        "shop_items": list_shop_items(db),
    }


def sell_item(db: Session, user_id: int, item_id: int, quantity: int) -> dict:
    if quantity <= 0:
        raise ValueError("La cantidad debe ser mayor que cero.")

    user = get_user(db, user_id)
    item = get_item(db, item_id)
    if user is None or item is None:
        raise ValueError("Usuario o item no encontrado.")

    user_item = get_user_item(db, user_id, item_id)
    if user_item is None or user_item.quantity < quantity:
        raise ValueError("No tienes suficientes unidades de ese item para vender.")

    user.gold += item.value * quantity
    update_user_item_quantity(db, user_item, user_item.quantity - quantity)

    shop_item = get_shop_item(db, item_id)
    if shop_item is None:
        create_shop_item(db, item_id, quantity)
    else:
        update_shop_item_quantity(db, shop_item, shop_item.quantity + quantity)

    db.commit()
    db.refresh(user)

    return {
        "user": user,
        "user_items": list_user_items(db, user_id),
        "shop_items": list_shop_items(db),
    }


def use_item_on_hero(db: Session, user_id: int, item_id: int, hero_id: int) -> dict:
    from app.crud.heroes import get_hero

    user_item = get_user_item(db, user_id, item_id)
    if not user_item or user_item.quantity <= 0:
        raise ValueError("No tienes este objeto.")

    item = get_item(db, item_id)
    if item is None or item.type.slug != "consumable":
        raise ValueError("Este objeto no es consumible.")

    hero = get_hero(db, hero_id)
    if hero is None:
        raise ValueError("Héroe no encontrado.")

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
