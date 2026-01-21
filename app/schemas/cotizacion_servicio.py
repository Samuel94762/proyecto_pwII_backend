from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, ForeignKey, Float


class CotizacionServicio(SQLModel, table=True):
    __tablename__ = "cotizaciones_servicios"
    id_cotizacion: int = Field(
        sa_column=Column(
            "id_cotizacion",
            Integer,
            ForeignKey("cotizaciones.id_cot"),
            primary_key=True,
        )
    )
    id_servicio: int = Field(
        sa_column=Column(
            "id_servicio",
            Integer,
            ForeignKey("servicios.id_ser"),
            primary_key=True,
        )
    )