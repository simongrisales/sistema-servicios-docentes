from django.db import models


class AsignacionModel(models.Model):
    grupo = models.ForeignKey(
        "academico.GrupoModel",
        on_delete=models.CASCADE,
        related_name="asignaciones",
    )
    aula = models.ForeignKey(
        "academico.AulaModel",
        on_delete=models.PROTECT,
        related_name="asignaciones",
    )
    bloque_horario = models.ForeignKey(
        "academico.HorarioBloqueModel",
        on_delete=models.CASCADE,
        related_name="asignaciones",
    )
    semestre = models.CharField(max_length=20)
    estado = models.CharField(max_length=50, default="CONFIRMADO")

    class Meta:
        db_table = "asignacion_asignacion"
        constraints = [
            models.UniqueConstraint(
                fields=["aula", "bloque_horario", "semestre"],
                name="uniq_aula_bloque_semestre",
            )
        ]


class ReglaNegocioModel(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    parametros = models.JSONField(default=dict, blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = "asignacion_regla_negocio"
        unique_together = ("tipo", "nombre")


class CatalogoParametroModel(models.Model):
    clave = models.CharField(max_length=100, unique=True)
    valor = models.JSONField(default=dict, blank=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "asignacion_catalogo_parametro"
