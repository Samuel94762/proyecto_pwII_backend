from fastapi import APIRouter
from app.core.database import CurrentContext
from app.schemas.cotizacion import CotizacionCreate, CotizacionUpdate, CotizacionRead
from app.schemas.common.response import ResponseObject, ResponseList
from app.handlers.cotizacion_handler import (
    handle_create_cotizacion,
    handle_get_cotizacion,
    handle_list_cotizaciones,
    handle_update_cotizacion,
    handle_delete_cotizacion,
)

router = APIRouter(tags=["COTIZACIONES"], prefix="/cotizaciones")


@router.get("/", response_model=ResponseList[CotizacionRead])
def list_cotizaciones(context: CurrentContext):
    """Lista todas las cotizaciones"""
    return handle_list_cotizaciones(context.current_session)


@router.get("/{id_cotizacion}", response_model=ResponseObject[CotizacionRead])
def get_cotizacion(id_cotizacion: int, context: CurrentContext):
    """Obtener una cotización por ID."""
    return handle_get_cotizacion(context.current_session, id_cotizacion)


@router.post("/", response_model=ResponseObject[CotizacionRead])
def create_cotizacion(context: CurrentContext, data: CotizacionCreate):
    """Crear una nueva cotización."""
    return handle_create_cotizacion(context, data)


@router.put("/{id_cotizacion}", response_model=ResponseObject[CotizacionRead])
def update_cotizacion(id_cotizacion: int, data: CotizacionUpdate, context: CurrentContext):
    """Actualizar una cotización por ID."""
    return handle_update_cotizacion(context, id_cotizacion, data)


@router.delete("/{id_cotizacion}")
def delete_cotizacion(id_cotizacion: int, context: CurrentContext):
    """Eliminar una cotización por ID."""
    return handle_delete_cotizacion(context, id_cotizacion)
