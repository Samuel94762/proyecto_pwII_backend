from fastapi import APIRouter
from app.core.database import CurrentContext
from app.schemas.trabajo import TrabajoCreate, TrabajoUpdate, TrabajoRead
from app.schemas.common.response import ResponseObject, ResponseList
from app.handlers.trabajo_handler import (
    handle_create_trabajo,
    handle_get_trabajo,
    handle_list_trabajos,
    handle_update_trabajo,
    handle_delete_trabajo,
)

router = APIRouter(tags=["TRABAJOS"], prefix="/trabajos")


@router.get("/", response_model=ResponseList[TrabajoRead])
def list_trabajos(context: CurrentContext):
    """Lista todos los trabajos"""
    return handle_list_trabajos(context.current_session)


@router.get("/{id_trabajo}", response_model=ResponseObject[TrabajoRead])
def get_trabajo(id_trabajo: int, context: CurrentContext):
    """Obtener un trabajo por ID."""
    return handle_get_trabajo(context.current_session, id_trabajo)


@router.post("/", response_model=ResponseObject[TrabajoRead])
def create_trabajo(context: CurrentContext, data: TrabajoCreate):
    """Crear un nuevo trabajo."""
    return handle_create_trabajo(context, data)


@router.put("/{id_trabajo}", response_model=ResponseObject[TrabajoRead])
def update_trabajo(id_trabajo: int, data: TrabajoUpdate, context: CurrentContext):
    """Actualizar un trabajo por ID."""
    return handle_update_trabajo(context, id_trabajo, data)


@router.delete("/{id_trabajo}")
def delete_trabajo(id_trabajo: int, context: CurrentContext):
    """Eliminar un trabajo por ID."""
    return handle_delete_trabajo(context, id_trabajo)