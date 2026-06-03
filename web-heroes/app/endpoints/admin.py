from datetime import datetime
from typing import Any
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.ddbb.database import get_db
from app.ddbb.Models import Enemy, Hero, HeroClass, HeroItem, Item, ItemType, Mission, User

router = APIRouter(tags=["backoffice"])
templates = Jinja2Templates(directory="app/templates")


TABLES: dict[str, dict[str, Any]] = {
    "users": {
        "label": "Usuarios",
        "model": User,
        "fields": {
            "name": {"type": "text", "required": True},
            "email": {"type": "text", "required": True},
            "password": {"type": "text"},
            "is_admin": {"type": "boolean"},
        },
    },
    "hero-classes": {
        "label": "Clases",
        "model": HeroClass,
        "fields": {
            "name": {"type": "text", "required": True},
            "base_hp_max": {"type": "int"},
            "base_mp_max": {"type": "int"},
            "default_race": {"type": "text"},
            "adjectives": {"type": "json-list"},
            "is_playable": {"type": "boolean"},
        },
    },
    "heroes": {
        "label": "Heroes",
        "model": Hero,
        "fields": {
            "user_id": {"type": "select", "model": User, "label_field": "email"},
            "hero_class_id": {"type": "select", "model": HeroClass, "label_field": "name"},
            "name": {"type": "text", "required": True},
            "hp_current": {"type": "int"},
            "mp_current": {"type": "int"},
            "energy_current": {"type": "int"},
            "experience": {"type": "int"},
            "level": {"type": "int"},
        },
    },
    "enemies": {
        "label": "Enemigos",
        "model": Enemy,
        "fields": {
            "name": {"type": "text", "required": True},
            "hero_class_id": {"type": "select", "model": HeroClass, "label_field": "name"},
            "level": {"type": "int"},
            "hp_max": {"type": "int", "required": True},
            "hp_current": {"type": "int"},
            "xp_reward": {"type": "int"},
            "is_boss": {"type": "boolean"},
        },
    },
    "item-types": {
        "label": "Tipos de item",
        "model": ItemType,
        "fields": {
            "name": {"type": "text", "required": True},
            "slug": {"type": "text", "required": True},
        },
    },
    "items": {
        "label": "Items",
        "model": Item,
        "fields": {
            "name": {"type": "text", "required": True},
            "item_type_id": {"type": "select", "model": ItemType, "label_field": "slug"},
            "sprite_x": {"type": "int"},
            "sprite_y": {"type": "int"},
            "hp_bonus": {"type": "int"},
            "mp_bonus": {"type": "int"},
            "damage_bonus": {"type": "int"},
            "price": {"type": "int"},
            "value": {"type": "int"},
            "thumbnail_url": {"type": "image"},
        },
    },
    "hero-items": {
        "label": "Equipo de heroes",
        "model": HeroItem,
        "fields": {
            "hero_id": {"type": "select", "model": Hero, "label_field": "name"},
            "item_id": {"type": "select", "model": Item, "label_field": "name"},
            "item_type_id": {"type": "select", "model": ItemType, "label_field": "slug"},
        },
    },
}


def table_config(table_name: str) -> dict[str, Any]:
    config = TABLES.get(table_name)
    if config is None:
        raise HTTPException(status_code=404, detail="Tabla no encontrada.")
    return config


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.isoformat(sep=" ", timespec="seconds")
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value)


def base_context(request: Request, active_table: str | None = None) -> dict[str, Any]:
    return {
        "request": request,
        "tables": TABLES,
        "active_table": active_table,
        "stringify": stringify,
    }


def select_options(db: Session, config: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    options: dict[str, list[dict[str, Any]]] = {}
    for field, meta in config["fields"].items():
        if meta["type"] != "select":
            continue
        rows = db.query(meta["model"]).order_by(meta["model"].id).all()
        options[field] = [
            {
                "value": row.id,
                "label": f'{row.id} - {getattr(row, meta["label_field"])}',
            }
            for row in rows
        ]
    return options


async def parse_payload(request: Request, config: dict[str, Any]) -> dict[str, Any]:
    raw = (await request.body()).decode()
    form = parse_qs(raw, keep_blank_values=True)
    data: dict[str, Any] = {}

    for field, meta in config["fields"].items():
        field_type = meta["type"]
        raw_value = form.get(field, [""])[0].strip()

        if field_type == "boolean":
            data[field] = field in form
        elif raw_value == "":
            if meta.get("required"):
                data[field] = raw_value
            continue
        elif field_type in {"int", "select"}:
            data[field] = int(raw_value)
        elif field_type == "json-list":
            data[field] = [part.strip() for part in raw_value.split(",")]
        else:
            data[field] = raw_value

    return data


def render_form(
    request: Request,
    db: Session,
    table_name: str,
    config: dict[str, Any],
    item: Any | None = None,
    error: str | None = None,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "backoffice/form.html",
        {
            **base_context(request, table_name),
            "title": f'Editar {config["label"]}' if item else f'Nuevo {config["label"]}',
            "table_name": table_name,
            "config": config,
            "item": item,
            "error": error,
            "select_options": select_options(db, config),
        },
    )


@router.post("/admin/reseed-combat-data")
def reseed_combat_data(db: Session = Depends(get_db)):
    """
    Delete all enemies and missions, then re-seed them with the updated seeders.
    User and hero data are preserved. Call this once after updating the seeders.
    """
    from app.ddbb.Seeders.EnemySeeder import seed_enemies
    from app.ddbb.Seeders.MissionSeeder import seed_missions

    db.query(Mission).delete()
    db.query(Enemy).delete()
    db.flush()

    classes = {hc.name: hc for hc in db.query(HeroClass).all()}
    enemies = seed_enemies(db, classes)
    seed_missions(db, enemies)
    db.commit()

    return JSONResponse({"status": "ok", "enemies_created": len(enemies)})


@router.get("/admin", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    cards = []
    for table_name, config in TABLES.items():
        cards.append(
            {
                "name": table_name,
                "label": config["label"],
                "count": db.query(config["model"]).count(),
            }
        )
    return templates.TemplateResponse(
        request,
        "backoffice/dashboard.html",
        {
            **base_context(request),
            "title": "Backoffice",
            "cards": cards,
        },
    )


@router.get("/admin/{table_name}", response_class=HTMLResponse)
def list_table(table_name: str, request: Request, db: Session = Depends(get_db)):
    config = table_config(table_name)
    rows = db.query(config["model"]).order_by(config["model"].id).all()
    fields = ["id", *config["fields"].keys()]
    return templates.TemplateResponse(
        request,
        "backoffice/list.html",
        {
            **base_context(request, table_name),
            "title": config["label"],
            "table_name": table_name,
            "config": config,
            "fields": fields,
            "rows": rows,
        },
    )


@router.get("/admin/{table_name}/new", response_class=HTMLResponse)
def new_item(table_name: str, request: Request, db: Session = Depends(get_db)):
    config = table_config(table_name)
    return render_form(request, db, table_name, config)


@router.post("/admin/{table_name}/new", response_class=HTMLResponse)
async def create_item(table_name: str, request: Request, db: Session = Depends(get_db)):
    config = table_config(table_name)
    data = await parse_payload(request, config)
    item = config["model"](**data)
    db.add(item)

    try:
        db.commit()
    except (IntegrityError, ValueError) as error:
        db.rollback()
        return render_form(request, db, table_name, config, error=str(error))

    return RedirectResponse(f"/admin/{table_name}", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/admin/{table_name}/{item_id}/edit", response_class=HTMLResponse)
def edit_item(table_name: str, item_id: int, request: Request, db: Session = Depends(get_db)):
    config = table_config(table_name)
    item = db.get(config["model"], item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado.")
    return render_form(request, db, table_name, config, item)


@router.post("/admin/{table_name}/{item_id}/edit", response_class=HTMLResponse)
async def update_item(table_name: str, item_id: int, request: Request, db: Session = Depends(get_db)):
    config = table_config(table_name)
    item = db.get(config["model"], item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado.")

    data = await parse_payload(request, config)
    for field, value in data.items():
        setattr(item, field, value)

    try:
        db.commit()
    except (IntegrityError, ValueError) as error:
        db.rollback()
        return render_form(request, db, table_name, config, item, str(error))

    return RedirectResponse(f"/admin/{table_name}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/admin/{table_name}/{item_id}/delete")
def delete_item(table_name: str, item_id: int, db: Session = Depends(get_db)):
    config = table_config(table_name)
    item = db.get(config["model"], item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado.")

    db.delete(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()

    return RedirectResponse(f"/admin/{table_name}", status_code=status.HTTP_303_SEE_OTHER)
