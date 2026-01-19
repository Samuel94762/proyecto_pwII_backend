from typing import Dict, List
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import Session
from app.core.database import CurrentContext
from app.schemas.trabajo import TrabajoCreate, TrabajoUpdate, TrabajoRead
from app.services.trabajo_services import (
    create_new_trabajo,
    get_active_trabajo_by_id,
    get_all_active_trabajos,
    update_existing_trabajo,
    save_trabajo_changes,
)


def handle_create_trabajo(context: CurrentContext, data: TrabajoCreate) -> Dict[str, object]:
    session = context.current_session
    trabajo = create_new_trabajo(session, data)
    save_trabajo_changes(session, trabajo)

    return {
        "data": TrabajoRead.model_validate(trabajo),
        "msg": "Trabajo creado exitosamente.",
    }


def handle_get_trabajo(session: Session, trabajo_id: int) -> Dict[str, object]:
    trabajo = get_active_trabajo_by_id(session, trabajo_id)
    if not trabajo:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado.")
    return {
        "data": TrabajoRead.model_validate(trabajo),
        "msg": "Trabajo obtenido exitosamente.",
    }


def handle_list_trabajos(session: Session) -> Dict[str, object]:
    trabajos = get_all_active_trabajos(session)
    return {"data": trabajos, "msg": "Trabajos obtenidos exitosamente."}


def handle_update_trabajo(
    context: CurrentContext, trabajo_id: int, data: TrabajoUpdate
) -> Dict[str, object]:
    session = context.current_session

    trabajo = get_active_trabajo_by_id(session, trabajo_id)
    if not trabajo:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado.")
    updated_trabajo = update_existing_trabajo(session, trabajo, data)
    save_trabajo_changes(session, trabajo)

    return {
        "data": TrabajoRead.model_validate(updated_trabajo),
        "msg": "Trabajo actualizado exitosamente",
    }


def handle_delete_trabajo(context: CurrentContext, trabajo_id: int) -> Dict[str, object]:
    session = context.current_session
    trabajo = get_active_trabajo_by_id(session, trabajo_id)
    if not trabajo:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado.")
    trabajo.is_deleted = True
    trabajo.deleted_at = datetime.now(timezone.utc)
    save_trabajo_changes(session, trabajo)
    return {"msg": "Trabajo eliminado exitosamente."}