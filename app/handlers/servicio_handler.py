from typing import Dict
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import Session
from app.core.database import CurrentContext
from app.schemas.servicio import ServicioCreate, ServicioUpdate, ServicioRead
from app.services.servicio_services import (
    create_new_servicio,
    get_active_servicio_by_id,
    get_all_active_servicios,
    update_existing_servicio,
    save_servicio_changes,
)


def handle_create_servicio(context: CurrentContext, data: ServicioCreate) -> Dict[str, object]:
    session = context.current_session
    servicio = create_new_servicio(session, data)
    save_servicio_changes(session, servicio)

    return {
        "data": ServicioRead.model_validate(servicio),
        "msg": "Servicio creado exitosamente.",
    }


def handle_get_servicio(session: Session, servicio_id: int) -> Dict[str, object]:
    servicio = get_active_servicio_by_id(session, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado.")
    return {
        "data": ServicioRead.model_validate(servicio),
        "msg": "Servicio obtenido exitosamente.",
    }


def handle_list_servicios(session: Session) -> Dict[str, object]:
    servicios = get_all_active_servicios(session)
    return {"data": servicios, "msg": "Servicios obtenidos exitosamente."}


def handle_update_servicio(
    context: CurrentContext, servicio_id: int, data: ServicioUpdate
) -> Dict[str, object]:
    session = context.current_session

    servicio = get_active_servicio_by_id(session, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado.")
    updated_servicio = update_existing_servicio(session, servicio, data)
    save_servicio_changes(session, servicio)

    return {
        "data": ServicioRead.model_validate(updated_servicio),
        "msg": "Servicio actualizado exitosamente",
    }


def handle_delete_servicio(context: CurrentContext, servicio_id: int) -> Dict[str, object]:
    session = context.current_session
    servicio = get_active_servicio_by_id(session, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado.")
    servicio.is_deleted = True
    servicio.deleted_at = datetime.now(timezone.utc)
    save_servicio_changes(session, servicio)
    return {"msg": "Servicio eliminado exitosamente."}