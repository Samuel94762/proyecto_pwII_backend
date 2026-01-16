from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, text


class Cliente(SQLModel, table=True):
    __tablename__ = "clientes"
    id: Optional[int] = Field(
        default=None, sa_column=Column("id_cli", Integer, primary_key=True)
    )
    nombre: str = Field(sa_column=Column("nombre_cli", String(255), nullable=False))
    apellido_paterno: str = Field(sa_column=Column("apellido_paterno_cli", String(255), nullable=False))
    apellido_materno: str = Field(sa_column=Column("apellido_materno_cli", String(255), nullable=False))
    telefono: Optional[str] = Field(
        default=None, sa_column=Column("telefono_cli", String(20), nullable=True)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "created_at_cli",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "updated_at_cli",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("deleted_at_cli", DateTime(timezone=True), nullable=True),
    )
    is_deleted: bool = Field(
        default=False,
        sa_column=Column("is_deleted_cli", Boolean, nullable=False, server_default="0"),
    )
    equipos: List["Equipo"] = Relationship(back_populates="dueno")
    cotizaciones: List["Cotizacion"] = Relationship(back_populates="cliente")
    
class ClienteCreate(SQLModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    telefono: Optional[str] = None

class ClienteUpdate(SQLModel):
    nombre: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    telefono: Optional[str] = None

class ClienteRead(SQLModel):
    id: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    telefono: Optional[str] = None
    created_at: datetime