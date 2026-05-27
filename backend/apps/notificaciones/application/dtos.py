# backend/apps/notificaciones/application/dtos.py
from datetime import datetime
from typing import List
from dataclasses import dataclass

@dataclass(frozen=True)
class CrearNotificacionInputDTO:
    """Datos de entrada para la creación de una notificación."""
    titulo: str
    mensaje: str
    tipo_notificacion: str # Debe coincidir con TiposNotificacion.CONFLICTO, etc.
    usuario_destino_id: str

@dataclass(frozen=True)
class MarcarLeidaInputDTO:
    """Dato de entrada para marcar una notificación como leída."""
    notificacion_id: str
    user_id: str

# DTOs de salida
@dataclass(frozen=True)
class NotificacionOutputDTO:
    """Representa los datos de la notificación tras ser recuperada exitosamente."""
    notificacion_id: str
    titulo: str
    mensaje: str
    fecha_creacion: datetime
    tipo: str
    es_leida: bool

@dataclass(frozen=True)
class ListaNotificacionesOutputDTO:
    """Contenedor para la lista de notificaciones."""
    notificaciones: List[NotificacionOutputDTO]