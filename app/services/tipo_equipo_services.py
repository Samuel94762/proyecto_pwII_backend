from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Session, select
from app.schemas.tipo_equipo import TipoEquipo, TipoEquipoCreate, TipoEquipoUpdate


def not_deleted():
    return TipoEquipo.is_deleted == False


def get_all_active_tipos(session: Session) -> List[TipoEquipo]:
    statement = select(TipoEquipo).where(not_deleted())
    return session.exec(statement).all()


def get_active_tipo_by_id(session: Session, tipo_id: int) -> Optional[TipoEquipo]:
    statement = select(TipoEquipo).where(TipoEquipo.id == tipo_id, not_deleted())
    return session.exec(statement).first()


def create_new_tipo(session: Session, data: TipoEquipoCreate) -> TipoEquipo:
    tipo = TipoEquipo(
        **data.model_dump(),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(tipo)
    session.flush()
    return tipo


def update_existing_tipo(
    session: Session, tipo: TipoEquipo, data: TipoEquipoUpdate
) -> TipoEquipo:
    update_dict = data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(tipo, key, value)
    tipo.updated_at = datetime.now(timezone.utc)
    session.add(tipo)
    session.flush()
    session.refresh(tipo)
    return tipo


def save_tipo_changes(session: Session, tipo: TipoEquipo) -> None:
    session.add(tipo)
    session.commit()
