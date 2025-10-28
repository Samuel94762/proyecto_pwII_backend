from typing import Optional
from datetime import datetime, timezone
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column, Integer, String, Boolean, DateTime, text


class Servicio(SQLModel, table=True):
    __tablename__ = "servicios"
    id: Optional[int] = Field(
        default=None, sa_column=Column("id_ser", Integer, primary_key=True)
    )
    nombre: str = Field(sa_column=Column("nombre_ser", String(255), nullable=False))
    descripcion: str = Field(sa_column=Column("descripcion_ser", String(255), nullable=False))
    precio: float = Field(sa_column=Column("precio_ser", String(255), nullable=False))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "created_at_ser",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "updated_at_ser",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("deleted_at_ser", DateTime(timezone=True), nullable=True),
    )
    is_deleted: bool = Field(
        default=False,
        sa_column=Column("is_deleted_ser", Boolean, nullable=False, server_default="0"),
    )
    
class ServicioCreate(SQLModel):
    nombre: str
    descripcion: str
    precio: float
    
class ServicioUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None

class ServicioRead(SQLModel):
    id: int
    nombre: str
    descripcion: str
    precio: float