from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..domain.entities import TipoNotificacion


class NotificacionModel(models.Model):
    """Modelo ORM para el catalogo operativo de notificaciones in-app."""

    class Tipo(models.TextChoices):
        ASIGNACION_COMPLETADA = (
            TipoNotificacion.ASIGNACION_COMPLETADA,
            _("Asignacion completada"),
        )
        CONFLICTO_DETECTADO = (
            TipoNotificacion.CONFLICTO_DETECTADO,
            _("Conflicto detectado"),
        )
        RESERVA_CONFIRMADA = (
            TipoNotificacion.RESERVA_CONFIRMADA,
            _("Reserva confirmada"),
        )
        RESERVA_EXPIRADA = (
            TipoNotificacion.RESERVA_EXPIRADA,
            _("Reserva expirada"),
        )

    notificacion_id = models.CharField(
        max_length=36,
        unique=True,
        db_index=True,
        verbose_name=_("ID de notificacion"),
    )
    tipo = models.CharField(
        max_length=32,
        choices=Tipo.choices,
        verbose_name=_("Tipo"),
    )
    titulo = models.CharField(max_length=255, verbose_name=_("Titulo"))
    mensaje = models.TextField(verbose_name=_("Mensaje"))
    usuario_destino = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificaciones_recibidas",
        verbose_name=_("Usuario destino"),
    )
    lectura_requerida = models.BooleanField(default=True, verbose_name=_("Requiere lectura"))
    es_leida = models.BooleanField(default=False, db_index=True, verbose_name=_("Leida"))
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_index=True)
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True, verbose_name=_("Activo"))

    class Meta:
        db_table = "notificaciones_notificacion"
        ordering = ["-fecha_creacion"]
        indexes = [
            models.Index(
                fields=["usuario_destino", "es_leida", "activo"],
                name="notif_usuario_estado_idx",
            )
        ]
        verbose_name = _("Notificacion")
        verbose_name_plural = _("Notificaciones")

    def __str__(self) -> str:
        return f"{self.titulo} -> {self.usuario_destino_id}"
