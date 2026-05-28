from django.conf import settings
from django.db import models

from ..domain.entities import TipoNotificacion


class NotificacionModel(models.Model):
    """Modelo ORM para el catalogo operativo de notificaciones in-app."""

    class Tipo(models.TextChoices):
        CONFLICTO = TipoNotificacion.CONFLICTO, "Conflicto"
        CONFIRMACION = TipoNotificacion.CONFIRMACION, "Confirmacion"
        ALERTA_MANTENIMIENTO = (
            TipoNotificacion.ALERTA_MANTENIMIENTO,
            "Alerta de mantenimiento",
        )
        INFO_USUARIO = TipoNotificacion.INFO_USUARIO, "Informacion de usuario"

    notificacion_id = models.CharField(max_length=36, unique=True, db_index=True)
    tipo = models.CharField(max_length=32, choices=Tipo.choices)
    titulo = models.CharField(max_length=255)
    mensaje = models.TextField()
    usuario_destino = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificaciones_recibidas",
    )
    lectura_requerida = models.BooleanField(default=True)
    es_leida = models.BooleanField(default=False, db_index=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_index=True)
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "notificaciones_notificacion"
        ordering = ["-fecha_creacion"]
        indexes = [
            models.Index(
                fields=["usuario_destino", "es_leida", "activo"],
                name="notif_usuario_estado_idx",
            )
        ]
        verbose_name = "Notificacion"
        verbose_name_plural = "Notificaciones"

    def __str__(self) -> str:
        return f"{self.titulo} -> {self.usuario_destino_id}"
