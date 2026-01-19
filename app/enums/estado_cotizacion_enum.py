from enum import Enum


class EstadoCotizacionEnum(str, Enum):
    ABIERTA = "Abierta"
    ACEPTADA = "Aceptada"
    RECHAZADA = "Rechazada"
    EXPIRADA = "Expirada"
    