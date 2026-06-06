from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def or_404(resource, detail: str = "Recurso no encontrado."):
    """Return resource if it exists, otherwise raise HTTP 404."""
    if resource is None:
        raise HTTPException(status_code=404, detail=detail)
    return resource


def integrity_error() -> HTTPException:
    return HTTPException(
        status_code=400,
        detail="No se pudo guardar el registro. Revisa claves foraneas, campos unicos o relaciones existentes.",
    )


def raise_integrity_error(error: IntegrityError) -> None:
    raise integrity_error() from error
