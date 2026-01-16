from enum import Enum
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, String,  Boolean, DateTime, text


class Tecnico(SQLModel, table=True):
    __tablename__ = "tecnicos"
    id: Optional[int] = Field(
        default=None, sa_column=Column("id_tec", Integer, primary_key=True)
    )
    nombre: str = Field(sa_column=Column("nombre_tec", String(255), nullable=False))
    apellido_paterno: str = Field(sa_column=Column("apellido_paterno_tec", String(255), nullable=False))
    apellido_materno: str = Field(sa_column=Column("apellido_materno_tec", String(255), nullable=False))
    telefono: Optional[str] = Field(sa_column=Column("telefono_tec", String(20), nullable=True))
    fecha_ingreso: Optional[datetime] = Field(
        default=None,
        sa_column=Column("fecha_ingreso_tec", DateTime(timezone=True), nullable=True),
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "created_at_tec",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "updated_at_tec",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("deleted_at_tec", DateTime(timezone=True), nullable=True),
    )
    is_deleted: bool = Field(
        default=False,
        sa_column=Column("is_deleted_tec", Boolean, nullable=False, server_default="0"),
    )
    trabajos: Optional["Trabajo"] = Relationship(back_populates="tecnico")
    cotizaciones: Optional["Cotizacion"] = Relationship(back_populates="tecnico")
    
class TecnicoCreate(SQLModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    telefono: Optional[str] = None
    fecha_ingreso: Optional[datetime] = None

class TecnicoUpdate(SQLModel):
    nombre: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    telefono: Optional[str] = None
    fecha_ingreso: Optional[datetime] = None

class TecnicoRead(SQLModel):
    id: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    telefono: Optional[str]
    fecha_ingreso: Optional[datetime]