# backend/apps/notificaciones/domain/entities.py

from datetime import datetime
from typing import List
# Importar posibles enums de sistema si se usan (Ejemplo: Rol)
# from sistemaserviciosdocentes.backend.core.models import RolModel

class TipoNotificacion:
    """Clase simple para definir tipos de notificaciones conocidas."""
    CONFLICTO = "conflict"        # Aula o recurso en conflicto con otro evento.
    CONFIRMACION = "confirmation"  # Una acción crítica fue confirmada (ej. asignación final).
    ALERTA_MANTENIMIENTO = "maintenance" # Aviso general del sistema.
    INFO_USUARIO = "user_info"    # Información relevante sobre el usuario o su cuenta.

class Notificacion:
    """Entidad de Dominio para una notificación."""
    def __init__(self,
                 notificacion_id: str,
                 tipo: str,
                 titulo: str,
                 mensaje: str,
                 fecha_creacion: datetime,
                 usuario_destino_id: str, # ID del usuario que recibirá la notificación
                 lectura_requerida: bool = True):
        self.notificacion_id = notificacion_id
        self.tipo = tipo
        self.titulo = titulo
        self.mensaje = mensaje
        self.fecha_creacion = fecha_creacion
        self.usuario_destino_id = usuario_destino_id
        self.lectura_requerida = lectura_requerida

    @classmethod
    def crear(cls, notification_id: str, tipo: str, titulo: str, mensaje: str, destino_id: str) -> 'Notificacion':
        """Método de fábrica para crear una notificación."""
        return cls(
            notification_id=notification_id,
            tipo=tipo,
            titulo=titulo,
            mensaje=mensaje,
            fecha_creacion=datetime.utcnow(), # Usar UTC para consistencia
            usuario_destino_id=destino_id
        )

# Nota: La lógica de "TipoNotificacion" y las constantes deben estar centralizadas en el proyecto core/enums si crece.