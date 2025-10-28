from enum import Enum


class EstadoEquipoEnum(str, Enum):
        PENDIENTE = "Pendiente"
        EN_REPARACION = "En Reparación"
        REPARADO = "Reparado"
        DEVUELTO = "Devuelto"
        ENTREGADO = "Entregado"
        CANCELADO = "Cancelado"