from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4


class TipoNotificacion:
    """Tipos institucionales soportados por el modulo de notificaciones."""

    ASIGNACION_COMPLETADA = "asignacion_completada"
    CONFLICTO_DETECTADO = "conflicto_detectado"
    RESERVA_CONFIRMADA = "reserva_confirmada"
    RESERVA_EXPIRADA = "reserva_expirada"

    # Alias de compatibilidad con nombres previos del sistema.
    CONFIRMACION = ASIGNACION_COMPLETADA
    CONFLICTO = CONFLICTO_DETECTADO
    ALERTA_MANTENIMIENTO = RESERVA_CONFIRMADA
    INFO_USUARIO = RESERVA_EXPIRADA

    @classmethod
    def values(cls) -> tuple[str, ...]:
        return (
            cls.ASIGNACION_COMPLETADA,
            cls.CONFLICTO_DETECTADO,
            cls.RESERVA_CONFIRMADA,
            cls.RESERVA_EXPIRADA,
            cls.CONFIRMACION,
            cls.CONFLICTO,
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
            fecha_creacion=datetime.now(UTC),
            usuario_destino_id=destino_id,
        )
