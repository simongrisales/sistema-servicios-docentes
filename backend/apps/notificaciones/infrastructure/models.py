# backend/apps/notificaciones/infrastructure/models.py

from django.db import models
from sistemaserviciosdocentes.backend.core.models import AbstractModel # Asumiendo la existencia de un modelo base Core
from systemserviciosdocentes.backend.apps.usuarios.domain.entities import Usuario # Referencia a entidad usuario para Foreign Key si aplica

class NotificacionModel(AbstractModel):
    """Modelo Django ORM para almacenar notificaciones."""

    # Campos de Identificación y Metadata
    UUID_NOTIFICACION = models.CharField("ID ÚNICO", max_length=36, unique=True) # UUID o hash único
    TIPO_CHOICES = [
        ('CONFLICTO', 'Conflicto'),
        ('CONFIRMACION', 'Confirmación'),
        ('ALERTA_MANTENIMIENTO', 'Alerta de Mantenimiento'),
        ('INFO_USUARIO', 'Info Usuario')
    ]
    TIPO = models.CharField(max_length=50, choices=TIPO_CHOICES)

    # Contenido
    TITULO = models.CharField(max_length=255)
    MENSAJE = models.TextField()

    # Destinatario y Estado
    USUARIO_DESTINO = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name="notificaciones_recibidas") # Foreign Key al usuario que recibe la alerta
    DESTAQUADO = models.BooleanField(default=False)
    ES_LEIDA = models.BooleanField(default=False)

    # Timestamps
    FECHA_CREACION = models.DateTimeField(auto_now_add=True)
    ESTADO_ACTIVO = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Notificación"
        ordering = ['-fecha_creacion'] # Más recientes primero

    # Método de utilidad para simular la creación (lo usarán los repositorios)
    @classmethod
    def create_raw(cls, notificacion_id: str, tipo: str, titulo: str, mensaje: str, usuario_destino: 'Usuario', destacado: bool = False):
        """Crea una instancia temporal sin guardar en DB para su uso interno."""
        return cls(
            UUID_NOTIFICACION=notificacion_id,
            TIPO=tipo,
            TITULO=titulo,
            MENSAJE=mensaje,
            USUARIO_DESTINO=usuario_destino,
            DESTAQUADO=destacado,
            ES_LEIDA=False
        )