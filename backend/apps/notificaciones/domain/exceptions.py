# backend/apps/notificaciones/domain/exceptions.py

from sistemaserviciosdocentes.backend.apps.core.domain.entities import SistemaError # Usar la excepción base del sistema

class NotificacionConflictoError(SistemaError):
    """Excepción lanzada cuando se intenta notificar sobre un evento que ya fue procesado o no tiene sentido."""
    pass

class UsuarioNoEncontradoError(SistemaError):
    """Lanzada si el usuario objetivo para la notificación no existe en el sistema."""
    pass

class TipoNotificacionInvalidoError(SistemaError):
    """Lanzada si se intenta usar un tipo de notificación desconocido o deshabilitado."""
    pass