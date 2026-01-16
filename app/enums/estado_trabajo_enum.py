from sqlmodel import Enum


class EstadoTrabajoEnum(str, Enum):
        RECIBIDO = "Recibido"
        EN_PROCESO = "En Proceso"
        COMPLETADO = "Completado"
        ENTREGADO = "Entregado"
        CANCELADO = "Cancelado"
        