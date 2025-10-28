from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Session, select
from app.schemas.servicio import Servicio, ServicioCreate, ServicioUpdate


def not_deleted():
    return Servicio.is_deleted == False


def get_all_active_servicios(session: Session) -> List[Servicio]:
    statement = select(Servicio).where(not_deleted())
    return session.exec(statement).all()


def get_active_servicio_by_id(session: Session, servicio_id: int) -> Optional[Servicio]:
    statement = select(Servicio).where(Servicio.id == servicio_id, not_deleted())
    return session.exec(statement).first()


def create_new_servicio(session: Session, data: ServicioCreate) -> Servicio:
    servicio = Servicio(
        **data.model_dump(),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(servicio)
    session.flush()
    return servicio


def update_existing_servicio(
    session: Session, servicio: Servicio, data: ServicioUpdate
) -> Servicio:
    update_dict = data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(servicio, key, value)
    servicio.updated_at = datetime.now(timezone.utc)
    session.add(servicio)
    session.flush()
    session.refresh(servicio)
    return servicio


def save_servicio_changes(session: Session, servicio: Servicio) -> None:
    session.add(servicio)
    session.commit()