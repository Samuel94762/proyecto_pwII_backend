from typing import Dict
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import Session
from app.core.database import CurrentContext
from app.schemas.cotizacion import CotizacionCreate, CotizacionUpdate, CotizacionRead
from app.services.cotizacion_services import (
    create_new_cotizacion,
    get_active_cotizacion_by_id,
    get_all_active_cotizaciones,
    update_existing_cotizacion,
    save_cotizacion_changes,
)


def handle_create_cotizacion(context: CurrentContext, data: CotizacionCreate) -> Dict[str, object]:
    session = context.current_session
    cotizacion = create_new_cotizacion(session, data)
    save_cotizacion_changes(session, cotizacion)

    return {
        "data": CotizacionRead.model_validate(cotizacion),
        "msg": "Cotización creada exitosamente.",
    }


def handle_get_cotizacion(session: Session, cotizacion_id: int) -> Dict[str, object]:
    cotizacion = get_active_cotizacion_by_id(session, cotizacion_id)
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada.")
    return {
        "data": CotizacionRead.model_validate(cotizacion),
        "msg": "Cotización obtenida exitosamente.",
    }


def handle_list_cotizaciones(session: Session) -> Dict[str, object]:
    cotizaciones = get_all_active_cotizaciones(session)
    return {"data": cotizaciones, "msg": "Cotizaciones obtenidas exitosamente."}


def handle_update_cotizacion(
    context: CurrentContext, cotizacion_id: int, data: CotizacionUpdate
) -> Dict[str, object]:
    session = context.current_session

    cotizacion = get_active_cotizacion_by_id(session, cotizacion_id)
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada.")
    updated_cotizacion = update_existing_cotizacion(session, cotizacion, data)
    save_cotizacion_changes(session, cotizacion)

    return {
        "data": CotizacionRead.model_validate(updated_cotizacion),
        "msg": "Cotización actualizada exitosamente",
    }

def handle_delete_cotizacion(context: CurrentContext, cotizacion_id: int) -> Dict[str, object]:
    session = context.current_session
    cotizacion = get_active_cotizacion_by_id(session, cotizacion_id)
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada.")
    cotizacion.is_deleted = True
    cotizacion.deleted_at = datetime.now(timezone.utc)
    save_cotizacion_changes(session, cotizacion)
    return {"msg": "Cotización eliminada exitosamente."}