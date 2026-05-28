# backend/apps/reportes/infrastructure/models.py
from django.db import models
from django.utils import timezone


class ReporteTipoModel(models.Model):
    """Modelo para almacenar los tipos de reportes configurables."""

    CODIGO_CHOICES = [
        ("OCCU", "Ocupación"),
        ("COV", "Cobertura Académica"),
        ("ASG", "Asignaciones Generales"),
    ]
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código")
    nombre_completo = models.CharField(max_length=255)
    descripcion = models.TextField()
    icono = models.CharField(
        max_length=50,
        help_text="Nombre de la clase CSS del icono (ej: fa-calendar-alt)",
    )

    class Meta:
        verbose_name = "Tipo de Reporte"
        verbose_name_plural = "Tipos de Reportes"

    def __str__(self):
        return f"{self.codigo} - {self.nombre_completo}"


class ReporteModel(models.Model):
    """Modelo que rastrea las peticiones y resultados de los reportes generados."""

    REPORTADO_CHOICES = [
        ("PENDIENTE", "Pendiente"),
        ("GENERANDO", "Generando"),
        ("COMPLETO", "Completo"),
        ("FALLIDO", "Fallido"),
    ]

    tipo = models.ForeignKey(
        ReporteTipoModel, on_delete=models.PROTECT, related_name="reportes_generados"
    )
    titulo = models.CharField(max_length=200)
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    periodo_inicio = models.DateField()
    periodo_fin = models.DateField()
    estado = models.CharField(
        max_length=10, choices=REPORTADO_CHOICES, default="PENDIENTE"
    )
    usuario_solicitante = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="reportes_solicitados",
    )
    datos_raw = models.JSONField(
        null=True, blank=True, verbose_name="Datos JSON crudos del reporte"
    )
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Reporte Generado"
        ordering = ["-fecha_solicitud"]

    def __str__(self):
        return f"{self.titulo} ({self.get_estado_display()})"
