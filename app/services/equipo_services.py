from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Session, select
from app.enums.estado_equipo_enum import EstadoEquipoEnum
from app.schemas.equipo import Equipo, EquipoCreate, EquipoUpdate


def not_deleted():
    return Equipo.is_deleted == False


def get_all_active_equipos(session: Session) -> List[Equipo]:
    statement = select(Equipo).where(not_deleted())
    return session.exec(statement).all()


def get_active_equipo_by_id(session: Session, equipo_id: int) -> Optional[Equipo]:
    statement = select(Equipo).where(Equipo.id == equipo_id, not_deleted())
    return session.exec(statement).first()


def create_new_equipo(session: Session, data: EquipoCreate) -> Equipo:
    equipo = Equipo(
        **data.model_dump(),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        estado=EstadoEquipoEnum.PENDIENTE,
    )
    session.add(equipo)
    session.flush()
    return equipo


def update_existing_equipo(
    session: Session, equipo: Equipo, data: EquipoUpdate
) -> Equipo:
    update_dict = data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(equipo, key, value)
    equipo.updated_at = datetime.now(timezone.utc)
    session.add(equipo)
    session.flush()
    session.refresh(equipo)
    return equipo


def save_equipo_changes(session: Session, equipo: Equipo) -> None:
    session.add(equipo)
    session.commit()
