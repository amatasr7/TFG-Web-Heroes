from sqlalchemy.orm import Session

from app.ddbb.Models import UserItem


def list_user_items(db: Session, user_id: int) -> list[UserItem]:
    return db.query(UserItem).filter(UserItem.user_id == user_id).order_by(UserItem.id).all()


def get_user_item(db: Session, user_id: int, item_id: int) -> UserItem | None:
    return (
        db.query(UserItem)
        .filter(UserItem.user_id == user_id, UserItem.item_id == item_id)
        .first()
    )


def create_user_item(db: Session, user_id: int, item_id: int, quantity: int) -> UserItem:
    user_item = UserItem(user_id=user_id, item_id=item_id, quantity=quantity)
    db.add(user_item)
    db.commit()
    db.refresh(user_item)
    return user_item


def update_user_item_quantity(db: Session, user_item: UserItem, quantity: int) -> UserItem | None:
    if quantity <= 0:
        db.delete(user_item)
        db.commit()
        return None
    user_item.quantity = quantity
    db.commit()
    db.refresh(user_item)
    return user_item
