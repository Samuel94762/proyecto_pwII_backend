from fastapi import APIRouter
from app.core.database import CurrentContext
from app.schemas.equipo import EquipoCreate, EquipoUpdate, EquipoRead
from app.schemas.common.response import ResponseObject, ResponseList
from app.handlers.equipo_handler import (
    handle_create_equipo,
    handle_get_equipo,
    handle_list_equipos,
    handle_update_equipo,
    handle_delete_equipo,
)

router = APIRouter(tags=["EQUIPOS"], prefix="/equipos")


@router.get("/", response_model=ResponseList[EquipoRead])
def list_equipos(context: CurrentContext):
    """Lista todos los equipos"""
    return handle_list_equipos(context.current_session)


@router.get("/{id_equipo}", response_model=ResponseObject[EquipoRead])
def get_equipo(id_equipo: int, context: CurrentContext):
    """Obtener un equipo por ID."""
    return handle_get_equipo(context.current_session, id_equipo)


@router.post("/", response_model=ResponseObject[EquipoRead])
def create_equipo(context: CurrentContext, data: EquipoCreate):
    """Crear un nuevo equipo."""
    return handle_create_equipo(context, data)


@router.put("/{id_equipo}", response_model=ResponseObject[EquipoRead])
def update_equipo(id_equipo: int, data: EquipoUpdate, context: CurrentContext):
    """Actualizar un equipo por ID."""
    return handle_update_equipo(context, id_equipo, data)


@router.delete("/{id_equipo}")
def delete_equipo(id_equipo: int, context: CurrentContext):
    """Eliminar un equipo por ID."""
    return handle_delete_equipo(context, id_equipo)
