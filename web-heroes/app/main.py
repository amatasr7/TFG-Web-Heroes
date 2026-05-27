from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.ddbb.database import Base, engine
from app.ddbb.schema import ensure_schema_updates
from app.ddbb.seed import seed_database
from app.endpoints import admin, combat, enemies, hero_classes, hero_items, heroes, item_types, items, users

app = FastAPI(title="Web Heroes API")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_schema_updates()
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
app.include_router(admin.router)
