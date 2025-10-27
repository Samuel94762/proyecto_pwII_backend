from fastapi import APIRouter
from app.core.context import CurrentContext
from app.filters.plant_filters import PlantFilterParams
from app.schemas.plant import PlantCreate, PlantUpdate
from app.schemas.common.response import ResponseObject, ResponseList
from app.schemas.plants.plant_read import PlantRead
from app.handlers.plant_handler import (
    handle_create_plant,
    handle_get_plant,
    handle_list_plants,
    handle_update_plant,
    handle_delete_plant,
)

router = APIRouter(tags=["CLIENTES"], prefix="/clientes")


@router.get("/", response_model=ResponseList[PlantRead])
def list_plants(context: CurrentContext, filters: PlantFilterParams):
    """Lista todos los clientes"""
    return handle_list_clientes(context.current_session, filters)


@router.get("/{id_cliente}", response_model=ResponseObject[PlantRead])
def get_plant(id_cliente: int, context: CurrentContext):
    """Obtener un cliente por ID."""
    return handle_get_cliente(context.current_session, id_cliente)


@router.post("/", response_model=ResponseObject[PlantRead])
def create_plant(context: CurrentContext, data: PlantCreate):
    """Crear un nuevo cliente."""
    return handle_create_cliente(context, data)


@router.put("/{id_cliente}", response_model=ResponseObject[PlantRead])
def update_plant(id_cliente: int, data: PlantUpdate, context: CurrentContext):
    """Actualizar un cliente por ID."""
    return handle_update_cliente(context, id_cliente, data)


@router.delete("/{id_cliente}")
def delete_plant(id_cliente: int, context: CurrentContext):
    """Eliminar un cliente por ID."""
    return handle_delete_cliente(context, id_cliente)