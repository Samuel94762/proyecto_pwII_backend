from typing import List, Optional
from datetime import datetime, timezone
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Boolean, Column, Integer, String, DateTime, text, ForeignKey

from app.enums.estado_cotizacion_enum import EstadoCotizacionEnum
from app.schemas.tecnico import TecnicoRead


class Trabajo(SQLModel, table=True):
    __tablename__ = "trabajos"
    id_tra: Optional[int] = Field(
        default=None, sa_column=Column("id_tra", Integer, primary_key=True)
    )
    descripcion: str = Field(
        sa_column=Column("descripcion_tra", String(255), nullable=False)
    )
    estado: str = Field(
        sa_column=Column("estado_tra", String(50), nullable=False)
    )
    estado: Optional[EstadoCotizacionEnum] = Field(
        default=None, sa_column=Column("estado_tra", String(255), nullable=True)
    )
    fecha_inicio: datetime = Field(
        sa_column=Column("fecha_inicio_tra", DateTime(timezone=True), nullable=False)
    )
    fecha_fin: Optional[datetime] = Field(
        default=None, sa_column=Column("fecha_fin_tra", DateTime(timezone=True), nullable=True)
    )
    costo: float = Field(
        sa_column=Column("costo_tra", String(255), nullable=False)
    )
    id_tecnico: int = Field(
        sa_column=Column("id_tecnico_tra", Integer, ForeignKey("tecnicos.id_tec"), nullable=False)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "created_at_tra",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "updated_at_tra",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    is_deleted: bool = Field(
        default=False,
        sa_column=Column("is_deleted_tra", Boolean, nullable=False, server_default="0"),
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("deleted_at_tra", DateTime(timezone=True), nullable=True),
    )
    tecnico: Optional["Tecnico"] = Relationship(back_populates="trabajos")
    
class TrabajoCreate(SQLModel):
    descripcion: str
    estado: str
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    costo: float
    id_tecnico: int
    
class TrabajoUpdate(SQLModel):
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    costo: Optional[float] = None
    id_tecnico: Optional[int] = None
    
class TrabajoRead(SQLModel):
    id_tra: int
    descripcion: str
    estado: str
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    costo: float
    tecnico: Optional[TecnicoRead]