class NotificacionError(Exception):
    """Error base controlado del dominio de notificaciones."""


class NotificacionConflictoError(NotificacionError):
    """Se lanza cuando una notificacion ya fue procesada o no aplica."""


class UsuarioNoEncontradoError(NotificacionError):
    """Se lanza cuando no existe el usuario destino."""


class TipoNotificacionInvalidoError(NotificacionError):
    """Se lanza cuando el tipo de notificacion no esta permitido."""
