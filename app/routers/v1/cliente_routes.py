from fastapi import APIRouter
from app.core.database import CurrentContext
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteRead
from app.schemas.common.response import ResponseObject, ResponseList
from app.handlers.cliente_handler import (
    handle_create_cliente,
    handle_get_cliente,
    handle_list_clientes,
    handle_update_cliente,
    handle_delete_cliente,
)

router = APIRouter(tags=["CLIENTES"], prefix="/clientes")


@router.get("/", response_model=ResponseList[ClienteRead])
def list_clientes(context: CurrentContext):
    """Lista todos los clientes"""
    return handle_list_clientes(context.current_session)


@router.get("/{id_cliente}", response_model=ResponseObject[ClienteRead])
def get_cliente(id_cliente: int, context: CurrentContext):
    """Obtener un cliente por ID."""
    return handle_get_cliente(context.current_session, id_cliente)


@router.post("/", response_model=ResponseObject[ClienteRead])
def create_cliente(context: CurrentContext, data: ClienteCreate):
    """Crear un nuevo cliente."""
    return handle_create_cliente(context, data)


@router.put("/{id_cliente}", response_model=ResponseObject[ClienteRead])
def update_cliente(id_cliente: int, data: ClienteUpdate, context: CurrentContext):
    """Actualizar un cliente por ID."""
    return handle_update_cliente(context, id_cliente, data)


@router.delete("/{id_cliente}")
def delete_cliente(id_cliente: int, context: CurrentContext):
    """Eliminar un cliente por ID."""
    return handle_delete_cliente(context, id_cliente)