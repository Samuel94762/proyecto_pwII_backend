from fastapi import APIRouter
from app.core.database import CurrentContext
from app.schemas.tecnico import TecnicoCreate, TecnicoUpdate, TecnicoRead
from app.schemas.common.response import ResponseObject, ResponseList
from app.handlers.tecnico_handler import (
    handle_create_tecnico,
    handle_get_tecnico,
    handle_list_tecnicos,
    handle_update_tecnico,
    handle_delete_tecnico,
)

router = APIRouter(tags=["TECNICOS"], prefix="/tecnicos")


@router.get("/", response_model=ResponseList[TecnicoRead])
def list_tecnicos(context: CurrentContext):
    """Lista todos los técnicos"""
    return handle_list_tecnicos(context.current_session)


@router.get("/{id_tecnico}", response_model=ResponseObject[TecnicoRead])
def get_tecnico(id_tecnico: int, context: CurrentContext):
    """Obtener un técnico por ID."""
    return handle_get_tecnico(context.current_session, id_tecnico)


@router.post("/", response_model=ResponseObject[TecnicoRead])
def create_tecnico(context: CurrentContext, data: TecnicoCreate):
    """Crear un nuevo técnico."""
    return handle_create_tecnico(context, data)


@router.put("/{id_tecnico}", response_model=ResponseObject[TecnicoRead])
def update_tecnico(id_tecnico: int, data: TecnicoUpdate, context: CurrentContext):
    """Actualizar un técnico por ID."""
    return handle_update_tecnico(context, id_tecnico, data)


@router.delete("/{id_tecnico}")
def delete_tecnico(id_tecnico: int, context: CurrentContext):
    """Eliminar un técnico por ID."""
    return handle_delete_tecnico(context, id_tecnico)