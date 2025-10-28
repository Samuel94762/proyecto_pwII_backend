from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Session, select
from app.schemas.tecnico import Tecnico, TecnicoCreate, TecnicoUpdate


def not_deleted():
    return Tecnico.is_deleted == False


def get_all_active_tecnicos(session: Session) -> List[Tecnico]:
    statement = select(Tecnico).where(not_deleted())
    return session.exec(statement).all()


def get_active_tecnico_by_id(session: Session, tecnico_id: int) -> Optional[Tecnico]:
    statement = select(Tecnico).where(Tecnico.id == tecnico_id, not_deleted())
    return session.exec(statement).first()


def create_new_tecnico(session: Session, data: TecnicoCreate) -> Tecnico:
    tecnico = Tecnico(
        **data.model_dump(),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(tecnico)
    session.flush()
    return tecnico


def update_existing_tecnico(
    session: Session, tecnico: Tecnico, data: TecnicoUpdate
) -> Tecnico:
    update_dict = data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(tecnico, key, value)
    tecnico.updated_at = datetime.now(timezone.utc)
    session.add(tecnico)
    session.flush()
    session.refresh(tecnico)
    return tecnico


def save_tecnico_changes(session: Session, tecnico: Tecnico) -> None:
    session.add(tecnico)
    session.commit()