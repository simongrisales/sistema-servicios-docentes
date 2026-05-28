from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4


class TipoNotificacion:
    """Tipos institucionales soportados por el modulo de notificaciones."""

    CONFLICTO = "conflict"
    CONFIRMACION = "confirmation"
    ALERTA_MANTENIMIENTO = "maintenance"
    INFO_USUARIO = "user_info"

    @classmethod
    def values(cls) -> tuple[str, ...]:
        return (
            cls.CONFLICTO,
            cls.CONFIRMACION,
            cls.ALERTA_MANTENIMIENTO,
            cls.INFO_USUARIO,
        )


@dataclass(frozen=True)
class Notificacion:
    """Entidad de dominio pura para una notificacion del sistema."""

    notificacion_id: str
    tipo: str
    titulo: str
    mensaje: str
    fecha_creacion: datetime
    usuario_destino_id: str
    lectura_requerida: bool = True
    es_leida: bool = False

    @classmethod
    def crear(
        cls,
        tipo: str,
        titulo: str,
        mensaje: str,
        destino_id: str,
        notification_id: str | None = None,
    ) -> "Notificacion":
        return cls(
            notificacion_id=notification_id or str(uuid4()),
            tipo=tipo,
            titulo=titulo,
            mensaje=mensaje,
            fecha_creacion=datetime.utcnow(),
            usuario_destino_id=destino_id,
        )
