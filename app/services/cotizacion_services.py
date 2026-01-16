from typing import Optional, List, Dict
from datetime import datetime, timezone
from sqlmodel import Session, select
from fastapi import HTTPException

from app.schemas.cotizacion import Cotizacion, CotizacionCreate, CotizacionUpdate
from app.schemas.equipo import Equipo
from app.schemas.cliente import Cliente
from app.schemas.tecnico import Tecnico
from app.enums.estado_cotizacion_enum import EstadoCotizacionEnum


def not_deleted():
    return Cotizacion.is_deleted == False


def get_all_active_cotizaciones(session: Session) -> List[Cotizacion]:
    statement = (
        select(Cotizacion)
        .where(not_deleted())
    )
    return session.exec(statement).all()


def get_active_cotizacion_by_id(session: Session, cotizacion_id: int) -> Optional[Cotizacion]:
    statement = (
        select(Cotizacion)
        .where(Cotizacion.id == cotizacion_id, not_deleted())
    )
    return session.exec(statement).first()


def validate_cotizacion_references(
    session: Session,
    cliente_id: int,
    equipo_id: int,
    tecnico_id: Optional[int] = None,
) -> Dict[str, any]:
    """Valida que existan las referencias a otras entidades y devuelve las entidades"""
    
    # Validar cliente
    cliente = session.get(Cliente, cliente_id)
    if not cliente or cliente.is_deleted:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
    # Validar equipo
    equipo = session.get(Equipo, equipo_id)
    if not equipo or equipo.is_deleted:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    
    # Validar que el equipo pertenezca al cliente
    if equipo.id_dueno != cliente_id:
        raise HTTPException(
            status_code=400,
            detail="El equipo no pertenece al cliente especificado",
        )
    
    # Validar técnico si se proporciona
    tecnico = None
    if tecnico_id:
        tecnico = session.get(Tecnico, tecnico_id)
        if not tecnico or tecnico.is_deleted:
            raise HTTPException(status_code=404, detail="Técnico no encontrado")
            
    return {"cliente": cliente, "equipo": equipo, "tecnico": tecnico}


def create_new_cotizacion(
    session: Session,
    data: CotizacionCreate,
) -> Cotizacion:
    # Validar referencias
    validate_cotizacion_references(
        session,
        data.id_cliente,
        data.id_equipo,
        data.id_tecnico,
    )
    
    # Crear cotización
    cotizacion = Cotizacion(
        **data.model_dump(),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        estado=EstadoCotizacionEnum.ABIERTA,
    )
    
    session.add(cotizacion)
    session.flush()
    return cotizacion


def update_existing_cotizacion(
    session: Session,
    cotizacion: Cotizacion,
    data: CotizacionUpdate,
) -> Cotizacion:
    update_dict = data.model_dump(exclude_unset=True)
    
    # Si se actualizan las referencias, validarlas
    if any(key in update_dict for key in ["id_cliente", "id_equipo", "id_tecnico"]):
        validate_cotizacion_references(
            session,
            update_dict.get("id_cliente", cotizacion.id_cliente),
            update_dict.get("id_equipo", cotizacion.id_equipo),
            update_dict.get("id_tecnico", cotizacion.id_tecnico),
        )
    
    # Actualizar campos
    for key, value in update_dict.items():
        setattr(cotizacion, key, value)
    
    cotizacion.updated_at = datetime.now(timezone.utc)
    session.add(cotizacion)
    session.flush()
    session.refresh(cotizacion)
    return cotizacion

def save_cotizacion_changes(session: Session, cotizacion: Cotizacion) -> None:
    session.add(cotizacion)
    session.commit()