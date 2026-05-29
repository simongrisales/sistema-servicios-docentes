"""Modelos Django ORM para la app parametros.

CatalogoParametroModel almacena parámetros del sistema con el campo
`valor` como JSONField (JSONB en PostgreSQL, TEXT JSON en SQLite).
"""

from django.db import models




class GrupoParametro(models.TextChoices):
    GENERAL = "general", "General"
    ASIGNACION = "asignacion", "Asignación"
    RESERVAS = "reservas", "Reservas"
    REPORTES = "reportes", "Reportes"
    NOTIFICACIONES = "notificaciones", "Notificaciones"
    SEGURIDAD = "seguridad", "Seguridad"


class CatalogoParametroModel(models.Model):
    """Parámetro de configuración del sistema.

    El campo `valor` es un JSONField, que en PostgreSQL se mapea
    automáticamente a tipo JSONB (binario, indexado, eficiente).
    En SQLite para tests, Django lo serializa como TEXT JSON.

    Ejemplo de uso:
        CatalogoParametroModel.objects.get(clave="max_aulas_por_semestre")
    """

    clave = models.CharField(
        max_length=120,
        unique=True,
        db_index=True,
        help_text="Identificador único del parámetro (snake_case).",
    )
    valor = models.JSONField(
        help_text=(
            "Valor estructurado del parámetro. "
            "Puede ser string, número, lista o dict."
        ),
    )
    grupo = models.CharField(
        max_length=50,
        choices=GrupoParametro.choices,
        default=GrupoParametro.GENERAL,
        db_index=True,
        help_text="Agrupación lógica del parámetro.",
    )
    descripcion = models.TextField(
        blank=True,
        default="",
        help_text="Descripción del propósito del parámetro.",
    )
    activo = models.BooleanField(
        default=True,
        help_text="Indica si el parámetro está vigente.",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "parametros_catalogo"
        ordering = ["grupo", "clave"]
        verbose_name = "Parámetro del catálogo"
        verbose_name_plural = "Parámetros del catálogo"

    def __str__(self) -> str:
        return f"{self.grupo}/{self.clave}"
