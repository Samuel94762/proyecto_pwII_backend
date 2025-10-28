from typing import Dict
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import Session
from app.core.database import CurrentContext
from app.schemas.tecnico import TecnicoCreate, TecnicoUpdate, TecnicoRead
from app.services.tecnico_services import (
    create_new_tecnico,
    get_active_tecnico_by_id,
    get_all_active_tecnicos,
    update_existing_tecnico,
    save_tecnico_changes,
)


def handle_create_tecnico(context: CurrentContext, data: TecnicoCreate) -> Dict[str, object]:
    session = context.current_session
    tecnico = create_new_tecnico(session, data)
    save_tecnico_changes(session, tecnico)

    return {
        "data": TecnicoRead.model_validate(tecnico),
        "msg": "Técnico creado exitosamente.",
    }


def handle_get_tecnico(session: Session, tecnico_id: int) -> Dict[str, object]:
    tecnico = get_active_tecnico_by_id(session, tecnico_id)
    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico no encontrado.")
    return {
        "data": TecnicoRead.model_validate(tecnico),
        "msg": "Técnico obtenido exitosamente.",
    }


def handle_list_tecnicos(session: Session) -> Dict[str, object]:
    tecnicos = get_all_active_tecnicos(session)
    return {"data": tecnicos, "msg": "Técnicos obtenidos exitosamente."}


def handle_update_tecnico(
    context: CurrentContext, tecnico_id: int, data: TecnicoUpdate
) -> Dict[str, object]:
    session = context.current_session

    tecnico = get_active_tecnico_by_id(session, tecnico_id)
    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico no encontrado.")
    updated_tecnico = update_existing_tecnico(session, tecnico, data)
    save_tecnico_changes(session, tecnico)

    return {
        "data": TecnicoRead.model_validate(updated_tecnico),
        "msg": "Técnico actualizado exitosamente",
    }


def handle_delete_tecnico(context: CurrentContext, tecnico_id: int) -> Dict[str, object]:
    session = context.current_session
    tecnico = get_active_tecnico_by_id(session, tecnico_id)
    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico no encontrado.")
    tecnico.is_deleted = True
    tecnico.deleted_at = datetime.now(timezone.utc)
    save_tecnico_changes(session, tecnico)
    return {"msg": "Técnico eliminado exitosamente."}