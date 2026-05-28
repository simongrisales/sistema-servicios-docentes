from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrearNotificacionInputDTO:
    titulo: str
    mensaje: str
    tipo_notificacion: str
    usuario_destino_id: str


@dataclass(frozen=True)
class MarcarLeidaInputDTO:
    notificacion_id: str
    user_id: str


@dataclass(frozen=True)
class NotificacionOutputDTO:
    notificacion_id: str
    titulo: str
    mensaje: str
    fecha_creacion: datetime
    tipo: str
    es_leida: bool


@dataclass(frozen=True)
class ListaNotificacionesOutputDTO:
    notificaciones: list[NotificacionOutputDTO]
