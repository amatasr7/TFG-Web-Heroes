from sqlalchemy import inspect, text

from app.ddbb.database import engine


def ensure_schema_updates() -> None:
    inspector = inspect(engine)
    if not inspector.has_table("items"):
        return

    item_columns = {column["name"] for column in inspector.get_columns("items")}
    if "thumbnail_url" in item_columns:
        return

    if engine.dialect.name == "mysql":
        statement = "ALTER TABLE items ADD COLUMN thumbnail_url VARCHAR(500) NULL"
    else:
        statement = "ALTER TABLE items ADD COLUMN thumbnail_url VARCHAR(500)"

    with engine.begin() as connection:
        connection.execute(text(statement))
