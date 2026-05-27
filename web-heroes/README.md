# Web Heroes Back-end

Este directorio contiene el back-end del proyecto `Web Heroes`.
Está construido con FastAPI, SQLAlchemy y utiliza SQLite por defecto.

## Estructura principal

- `app/main.py` - Punto de entrada de la aplicación.
- `app/ddbb/` - Configuración de base de datos, modelos y semilla inicial.
- `app/endpoints/` - Definición de rutas HTTP y controladores.
- `app/crud/` - Lógica de acceso a datos (CRUD) separada de los endpoints.
- `app/schemas/` - Esquemas Pydantic para validación de entrada y serialización de salida.
- `app/static/` - Archivos estáticos usados por el panel de administración.
- `app/templates/backoffice/` - Plantillas Jinja para el backoffice.
- `data/web_heroes.sqlite3` - Base de datos SQLite generada.

## `app/main.py`

`main.py` crea la aplicación FastAPI y configura:

- CORS abierto para permitir llamadas desde front-end.
- Montaje de archivos estáticos en `/static`.
- Evento `startup` que:
    - crea las tablas necesarias (`Base.metadata.create_all(bind=engine)`).
    - ejecuta actualizaciones de esquema con `ensure_schema_updates()`.
    - carga datos iniciales con `seed_database()`.
- Rutas básicas:
    - `/` - mensaje de confirmación.
    - `/health` - estado del servicio.

Además incluye los routers de las distintas áreas con el prefijo `/api` y el router de administrador sin prefijo.

## Base de datos

### `app/ddbb/database.py`

- Usa `DATABASE_URL` de `.env` o el valor por defecto `sqlite:///./data/web_heroes.sqlite3`.
- Crea el motor SQLAlchemy y la sesión.
- Define `Base` como la clase base declarativa.
- Proporciona `get_db()` para inyectar sesiones en los endpoints.

### `app/ddbb/models.py`

Define las tablas principales del juego:

- `User` - usuarios del sistema, con campo `is_admin`.
- `HeroClass` - clases de héroe/enemigo.
- `Hero` - personajes jugables y su progreso.
- `Enemy` - enemigos con estadísticas y recompensa de XP.
- `ItemType` - tipo de ítem.
- `Item` - elementos equipables o consumibles.
- `HeroItem` - relación entre héroe, ítem y tipo de ítem.

### `app/ddbb/schema.py`

- Verifica si la tabla `items` existe.
- Agrega la columna `thumbnail_url` si no está presente.
- Permite migraciones simples sin herramientas externas.

### `app/ddbb/seed.py`

- Inserta datos iniciales si la base de datos está vacía.
- Crea un usuario de prueba administrador.
- Crea clases de héroe (`Guerrero`, `Mago`, `Picaro`, `Jefe`).
- Crea tipos de items e items con estadísticas iniciales.
- Crea héroes de ejemplo y enemigos.

## API REST

Los endpoints CRUD se organizan por recurso, y cada archivo en `app/endpoints/` define un router.

Rutas principales disponibles:

- `/api/users` - gestión de usuarios.
- `/api/heroes` - gestión de héroes.
- `/api/enemies` - gestión de enemigos.
- `/api/items` - gestión de items.
- `/api/hero-classes` - gestión de clases.
- `/api/item-types` - gestión de tipos de item.
- `/api/hero-items` - gestión de items asignados a héroes.
- `/api/combat/attack/{hero_id}/{enemy_id}` - acción de combate entre un héroe y un enemigo.

Cada endpoint sigue el patrón:

- `GET /resource` - lista recursos.
- `GET /resource/{id}` - obtiene un recurso.
- `POST /resource` - crea un recurso.
- `PUT /resource/{id}` - reemplaza un recurso.
- `PATCH /resource/{id}` - actualiza parcialmente un recurso.
- `DELETE /resource/{id}` - borra un recurso.

## Separación de responsabilidades

- `app/endpoints/` se encarga de recibir solicitudes HTTP, validar parámetros y manejar respuestas.
- `app/crud/` contiene funciones genéricas y específicas para acceder a la base de datos.
- `app/schemas/` define los modelos de datos utilizados en validación y serialización.

Ejemplo de flujo:

1. Un cliente llama a `POST /api/hero-items`.
2. El endpoint en `app/endpoints/hero_items.py` recibe el payload y abre sesión con `get_db()`.
3. El endpoint llama a `create_hero_item()` en `app/crud/hero_items.py`.
4. La función CRUD usa SQLAlchemy para crear el registro y devuelve el objeto.
5. FastAPI serializa la respuesta usando `HeroItemRead`.

## Panel de administración

`app/endpoints/admin.py` expone un panel de administración accesible en `/admin`.

- Usa plantillas Jinja desde `app/templates/backoffice/`.
- Permite listar, crear, editar y eliminar registros de las tablas soportadas.
- Se sirve un CSS específico desde `app/static/backoffice.css`.

## Contenedores y ejecución

### `Dockerfile`

- Base: `python:3.13-slim`.
- Instala dependencias desde `requirements.txt`.
- Copia `app/` al contenedor.
- Expone el puerto `8000`.
- Ejecuta `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

### Dependencias

Definidas en `requirements.txt`:

- `fastapi`
- `uvicorn[standard]`
- `sqlalchemy`
- `pydantic`
- `python-dotenv`
- `pymysql`
- `cryptography`
- `jinja2`

## Cómo usar

1. Copia o configura `.env` si necesitas cambiar `DATABASE_URL`.
2. Ejecuta el contenedor o inicia `uvicorn` localmente desde `app/main.py`.
3. Accede a la API en `http://localhost:8000`.
4. Los endpoints de la API están bajo `/api`.
5. El panel de administración está en `/admin`.

## Notas importantes

- La base de datos por defecto es SQLite local en `data/web_heroes.sqlite3`.
- `seed_database()` solo inserta datos la primera vez si no existen clases de héroe.
- El back-end también admite migración simple para `thumbnail_url` en la tabla `items`.
