import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.ddbb.database import Base, engine
from app.ddbb.seed import seed_database
from app.endpoints import admin, combat, enemies, hero_classes, hero_items, heroes, item_types, items, missions, shop, users, warbands
from app.endpoints.admin import AdminNotAuthenticated

app = FastAPI(title="Web Heroes API")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "wh-backoffice-dev-secret"),
)


@app.exception_handler(AdminNotAuthenticated)
async def admin_not_authenticated(_request: Request, _exc: AdminNotAuthenticated) -> RedirectResponse:
    return RedirectResponse("/admin/login", status_code=303)

@app.on_event("startup")
def on_startup() -> None:
    import app.ddbb.Models  # noqa: F401 — registers all models with Base
    Base.metadata.create_all(engine)
    seed_database()

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Web Heroes API"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(combat.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(heroes.router, prefix="/api")
app.include_router(enemies.router, prefix="/api")
app.include_router(items.router, prefix="/api")
app.include_router(hero_classes.router, prefix="/api")
app.include_router(item_types.router, prefix="/api")
app.include_router(hero_items.router, prefix="/api")
app.include_router(missions.router, prefix="/api")
app.include_router(warbands.router, prefix="/api")
app.include_router(shop.router, prefix="/api")
app.include_router(admin.public_router)
app.include_router(admin.router)
