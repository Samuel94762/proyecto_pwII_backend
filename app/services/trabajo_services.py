from typing import Dict, Optional, List
from datetime import datetime, timezone
from sqlmodel import Session, select
from fastapi import HTTPException
from app.schemas.trabajo import Trabajo, TrabajoCreate, TrabajoUpdate
from app.schemas.tecnico import Tecnico


def not_deleted():
    return Trabajo.is_deleted == False


def get_all_active_trabajos(session: Session) -> List[Trabajo]:
    statement = (
        select(Trabajo)
        .where(not_deleted())
    )
    return session.exec(statement).all()


def get_active_trabajo_by_id(session: Session, trabajo_id: int) -> Optional[Trabajo]:
    statement = (
        select(Trabajo)
        .where(Trabajo.id_tra == trabajo_id, not_deleted())
    )
    return session.exec(statement).first()


def validate_trabajo_references(
    session: Session,
    tecnico_id: int,
) -> Dict[str, any]:
    """Valida que existan las referencias a otras entidades y devuelve las entidades"""
    
    # Validar técnico
    tecnico = session.get(Tecnico, tecnico_id)
    if not tecnico or tecnico.is_deleted:
        raise HTTPException(status_code=404, detail="Técnico no encontrado")
            
    return {"tecnico": tecnico}


def create_new_trabajo(session: Session, data: TrabajoCreate) -> Trabajo:
    # Validar referencias
    validate_trabajo_references(session, data.id_tecnico)
    
    # Crear trabajo
    trabajo = Trabajo(
        **data.model_dump(),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    
    session.add(trabajo)
    session.flush()
    return trabajo


def update_existing_trabajo(
    session: Session, trabajo: Trabajo, data: TrabajoUpdate
) -> Trabajo:
    update_dict = data.model_dump(exclude_unset=True)
    
    # Si se actualiza el técnico, validar que exista
    if "id_tecnico" in update_dict:
        validate_trabajo_references(session, update_dict["id_tecnico"])
    
    for key, value in update_dict.items():
        setattr(trabajo, key, value)
    
    trabajo.updated_at = datetime.now(timezone.utc)
    session.add(trabajo)
    session.flush()
    session.refresh(trabajo)
    return trabajo


def save_trabajo_changes(session: Session, trabajo: Trabajo) -> None:
    session.add(trabajo)
    session.commit()