# Web Heroes Back-end

Este directorio contiene el back-end del proyecto `Web Heroes`.
Esta construido con FastAPI, SQLAlchemy y Alembic.

## Estructura principal

- `app/main.py` - Punto de entrada de la aplicacion.
- `app/ddbb/` - Configuracion de base de datos, modelos y semilla inicial.
- `app/endpoints/` - Rutas HTTP y controladores.
- `app/crud/` - Logica de acceso a datos.
- `app/schemas/` - Esquemas Pydantic para entrada y salida de la API.
- `alembic/` - Migraciones de base de datos.
- `alembic.ini` - Configuracion de Alembic.

## Base de datos

`app/ddbb/database.py` lee `DATABASE_URL` desde `.env` o usa por defecto:

```txt
sqlite:///./data/web_heroes.sqlite3
```

Los modelos SQLAlchemy viven en `app/ddbb/models.py`. Alembic usa esos modelos para autogenerar migraciones mediante `Base.metadata`.

## Migraciones

Para una base de datos nueva:

```bash
alembic upgrade head
```

Para una base de datos existente que ya fue creada con `create_all`, marca una sola vez el estado actual:

```bash
alembic stamp head
```

Despues, usa migraciones normales.

## Flujo de cambios de base de datos

Cuando quieras cambiar columnas, tablas, indices o relaciones:

1. Edita los modelos SQLAlchemy en `app/ddbb/models.py`.
2. Si cambia la API, actualiza tambien los esquemas Pydantic en `app/schemas/`.
3. Genera una migracion:

```bash
alembic revision --autogenerate -m "describe el cambio"
```

4. Revisa el archivo creado en `alembic/versions/`.
5. Aplica la migracion:

```bash
alembic upgrade head
```

En Docker, el backend ejecuta `alembic upgrade head` automaticamente antes de arrancar FastAPI.

## Arranque local

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

La API queda en `http://localhost:8000` y las rutas principales estan bajo `/api`.
El panel de administracion esta en `/admin`.

## Docker

El servicio `backend` usa `DATABASE_URL` desde `docker-compose.yml`:

```txt
mysql+pymysql://webheroes:webheroes@db:3306/webheroes
```

Al arrancar el contenedor, primero se aplican las migraciones y despues se levanta `uvicorn`.

## Datos iniciales

`seed_database()` se ejecuta al arrancar la aplicacion. Solo inserta datos iniciales cuando no existen clases de heroe, por lo que no sustituye a Alembic ni modifica el esquema.
