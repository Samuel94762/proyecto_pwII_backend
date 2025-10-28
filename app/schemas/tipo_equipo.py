from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, text

class TipoEquipo(SQLModel, table=True):
    __tablename__ = "tipos_equipo"
    id: Optional[int] = Field(
        default=None, sa_column=Column("id_teq", Integer, primary_key=True)
    )
    nombre: str = Field(sa_column=Column("nombre_teq", String(255), nullable=False))
    descripcion: str = Field(sa_column=Column("descripcion_teq", String(255), nullable=False))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "created_at_teq",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "updated_at_teq",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("deleted_at_teq", DateTime(timezone=True), nullable=True),
    )
    is_deleted: bool = Field(
        default=False,
        sa_column=Column("is_deleted_teq", Boolean, nullable=False, server_default="0"),
    )
    equipos: List["Equipo"] = Relationship(back_populates="tipo_equipo")
    
class TipoEquipoRead(SQLModel):
    id: int
    nombre: str
    descripcion: str

class TipoEquipoCreate(SQLModel):
    nombre: str
    descripcion: str

class TipoEquipoUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None