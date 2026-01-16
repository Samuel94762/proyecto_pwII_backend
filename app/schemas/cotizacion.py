from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, text

from app.enums.estado_cotizacion_enum import EstadoCotizacionEnum

if TYPE_CHECKING:
    from app.schemas.trabajo import Trabajo
    from app.schemas.cliente import Cliente
    from app.schemas.equipo import Equipo
    from app.schemas.tecnico import Tecnico
from app.schemas.cotizacion_servicio import CotizacionServicio
from app.schemas.equipo import EquipoRead
from app.schemas.cliente import ClienteRead
from app.schemas.tecnico import TecnicoRead
from app.schemas.trabajo import TrabajoRead


class Cotizacion(SQLModel, table=True):
    __tablename__ = "cotizaciones"
    id: Optional[int] = Field(
        default=None, sa_column=Column("id_cot", Integer, primary_key=True)
    )
    id_cliente: int = Field(
        sa_column=Column("id_cliente_cot", Integer, ForeignKey("clientes.id_cli"))
    )
    descripcion_falla: str = Field(sa_column=Column("descripcion_falla_cot", String(255), nullable=False))
    diagnostico: Optional[str] = Field(sa_column=Column("diagnostico_cot", String(255), nullable=True))
    fecha_expiracion: Optional[datetime] = Field(
        default=None,
        sa_column=Column("fecha_expiracion_cot", DateTime(timezone=True), nullable=True),
    )
    id_tecnico: Optional[int] = Field(
        default=None,
        sa_column=Column("id_tecnico_cot", Integer, ForeignKey("tecnicos.id_tec")),
    )
    estado: Optional[EstadoCotizacionEnum] = Field(
        default=None, sa_column=Column("estado_cot", String(255), nullable=True)
    )
    precio_total: Optional[float] = Field(
        default=None, sa_column=Column("precio_total_cot", String(255), nullable=True)
    )
    id_equipo: int = Field(
        sa_column=Column("id_equipo_cot", Integer, ForeignKey("equipos.id_equ"), nullable=True)
    )
    id_trabajo: Optional[int] = Field(
        default=None,
        sa_column=Column("id_trabajo_cot", Integer, ForeignKey("trabajos.id_tra"), nullable=True),
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "created_at_cot",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "updated_at_cot",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("deleted_at_cot", DateTime(timezone=True), nullable=True),
    )
    is_deleted: bool = Field(
        default=False,
        sa_column=Column("is_deleted_cot", Boolean, nullable=False, server_default="0"),
    )
    equipo: Optional["Equipo"] = Relationship(back_populates="cotizaciones")
    cliente: Optional["Cliente"] = Relationship(back_populates="cotizaciones")
    tecnico: Optional["Tecnico"] = Relationship(back_populates="cotizaciones")
    
class CotizacionCreate(SQLModel):
    id_cliente: int
    descripcion_falla: str
    diagnostico: Optional[str] = None
    id_equipo: int
    fecha_expiracion: Optional[datetime] = None
    id_tecnico: Optional[int] = None
    precio_total: Optional[float] = None
    id_trabajo: Optional[int] = None
    
class CotizacionUpdate(SQLModel):
    id_cliente: Optional[int] = None
    descripcion_falla: Optional[str] = None
    diagnostico: Optional[str] = None
    fecha_expiracion: Optional[datetime] = None
    id_tecnico: Optional[int] = None
    estado: Optional[EstadoCotizacionEnum] = None
    precio_total: Optional[float] = None
    id_equipo: Optional[int] = None
    id_trabajo: Optional[int] = None
    created_at: Optional[datetime] = None

class CotizacionRead(SQLModel):
    id: int
    descripcion_falla: str
    diagnostico: Optional[str]
    fecha_expiracion: Optional[datetime]
    tecnico: Optional[TecnicoRead]
    estado: Optional[EstadoCotizacionEnum]
    precio_total: Optional[float]
    equipo: Optional[EquipoRead]
    cliente: Optional[ClienteRead]
    servicios: Optional[List[CotizacionServicio]] = None
    created_at: Optional[datetime]
    id_trabajo: Optional[int]

