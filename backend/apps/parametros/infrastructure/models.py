"""Modelos Django ORM para la app parametros.

CatalogoParametroModel almacena parametros del sistema con el campo
`valor` como JSONField (JSONB en PostgreSQL, TEXT JSON en SQLite).
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class GrupoParametro(models.TextChoices):
    GENERAL = "general", _("General")
    ASIGNACION = "asignacion", _("Asignacion")
    RESERVAS = "reservas", _("Reservas")
    REPORTES = "reportes", _("Reportes")
    NOTIFICACIONES = "notificaciones", _("Notificaciones")
    SEGURIDAD = "seguridad", _("Seguridad")


class CatalogoParametroModel(models.Model):
    """Parametro de configuracion del sistema."""

    clave = models.CharField(
        max_length=120,
        unique=True,
        db_index=True,
        help_text=_("Identificador unico del parametro (snake_case)."),
        verbose_name=_("Clave"),
    )
    valor = models.JSONField(
        help_text=_(
            "Valor estructurado del parametro. Puede ser string, numero, lista o dict."
        ),
        verbose_name=_("Valor"),
    )
    grupo = models.CharField(
        max_length=50,
        choices=GrupoParametro.choices,
        default=GrupoParametro.GENERAL,
        db_index=True,
        help_text=_("Agrupacion logica del parametro."),
        verbose_name=_("Grupo"),
    )
    descripcion = models.TextField(
        blank=True,
        default="",
        help_text=_("Descripcion del proposito del parametro."),
        verbose_name=_("Descripcion"),
    )
    activo = models.BooleanField(
        default=True,
        help_text=_("Indica si el parametro esta vigente."),
        verbose_name=_("Activo"),
    )
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name=_("Creado en"))
    actualizado_en = models.DateTimeField(
        auto_now=True, verbose_name=_("Actualizado en")
    )

    class Meta:
        db_table = "parametros_catalogo"
        ordering = ["grupo", "clave"]
        verbose_name = _("Parametro del catalogo")
        verbose_name_plural = _("Parametros del catalogo")

    def __str__(self) -> str:
        return f"{self.grupo}/{self.clave}"
