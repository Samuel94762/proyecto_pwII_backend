from fastapi import APIRouter
from app.core.database import CurrentContext
from app.schemas.servicio import ServicioCreate, ServicioUpdate, ServicioRead
from app.schemas.common.response import ResponseObject, ResponseList
from app.handlers.servicio_handler import (
    handle_create_servicio,
    handle_get_servicio,
    handle_list_servicios,
    handle_update_servicio,
    handle_delete_servicio,
)

router = APIRouter(tags=["SERVICIOS"], prefix="/servicios")


@router.get("/", response_model=ResponseList[ServicioRead])
def list_servicios(context: CurrentContext):
    """Lista todos los servicios"""
    return handle_list_servicios(context.current_session)


@router.get("/{id_servicio}", response_model=ResponseObject[ServicioRead])
def get_servicio(id_servicio: int, context: CurrentContext):
    """Obtener un servicio por ID."""
    return handle_get_servicio(context.current_session, id_servicio)


@router.post("/", response_model=ResponseObject[ServicioRead])
def create_servicio(context: CurrentContext, data: ServicioCreate):
    """Crear un nuevo servicio."""
    return handle_create_servicio(context, data)


@router.put("/{id_servicio}", response_model=ResponseObject[ServicioRead])
def update_servicio(id_servicio: int, data: ServicioUpdate, context: CurrentContext):
    """Actualizar un servicio por ID."""
    return handle_update_servicio(context, id_servicio, data)


@router.delete("/{id_servicio}")
def delete_servicio(id_servicio: int, context: CurrentContext):
    """Eliminar un servicio por ID."""
    return handle_delete_servicio(context, id_servicio)