from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Session, select
from app.schemas.cliente import Cliente, ClienteCreate, ClienteUpdate


def not_deleted():
    return Cliente.is_deleted == False


def get_all_active_clientes(session: Session) -> List[Cliente]:
    statement = select(Cliente).where(not_deleted())
    return session.exec(statement).all()


def get_active_cliente_by_id(session: Session, cliente_id: int) -> Optional[Cliente]:
    statement = select(Cliente).where(Cliente.id == cliente_id, not_deleted())
    return session.exec(statement).first()


def create_new_cliente(session: Session, data: ClienteCreate) -> Cliente:
    cliente = Cliente(
        **data.model_dump(),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(cliente)
    session.flush()
    return cliente


def update_existing_cliente(
    session: Session, cliente: Cliente, data: ClienteUpdate
) -> Cliente:
    update_dict = data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(cliente, key, value)
    cliente.updated_at = datetime.now(timezone.utc)
    session.add(cliente)
    session.flush()
    session.refresh(cliente)
    return cliente


def save_cliente_changes(session: Session, cliente: Cliente) -> None:
    session.add(cliente)
    session.commit()