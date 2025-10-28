from fastapi import APIRouter
from app.core.database import CurrentContext
from app.schemas.tipo_equipo import TipoEquipoCreate, TipoEquipoUpdate, TipoEquipoRead
from app.schemas.common.response import ResponseObject, ResponseList
from app.handlers.tipo_equipo_handler import (
    handle_create_tipo,
    handle_get_tipo,
    handle_list_tipos,
    handle_update_tipo,
    handle_delete_tipo,
)

router = APIRouter(tags=["TIPOS_EQUIPO"], prefix="/tipos_equipo")


@router.get("/", response_model=ResponseList[TipoEquipoRead])
def list_tipos(context: CurrentContext):
    """Lista todos los tipos de equipo"""
    return handle_list_tipos(context.current_session)


@router.get("/{id_tipo}", response_model=ResponseObject[TipoEquipoRead])
def get_tipo(id_tipo: int, context: CurrentContext):
    """Obtener un tipo por ID."""
    return handle_get_tipo(context.current_session, id_tipo)


@router.post("/", response_model=ResponseObject[TipoEquipoRead])
def create_tipo(context: CurrentContext, data: TipoEquipoCreate):
    """Crear un nuevo tipo de equipo."""
    return handle_create_tipo(context, data)


@router.put("/{id_tipo}", response_model=ResponseObject[TipoEquipoRead])
def update_tipo(id_tipo: int, data: TipoEquipoUpdate, context: CurrentContext):
    """Actualizar un tipo por ID."""
    return handle_update_tipo(context, id_tipo, data)


@router.delete("/{id_tipo}")
def delete_tipo(id_tipo: int, context: CurrentContext):
    """Eliminar un tipo por ID."""
    return handle_delete_tipo(context, id_tipo)
