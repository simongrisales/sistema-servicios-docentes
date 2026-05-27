from django.db import models
# Se asume que existen modelos de las apps dependientes (academico)
from apps.academico.infrastructure.models import AulaModel, GrupoModel, HorarioBloqueModel

class AsignacionModel(models.Model):
    """Modelo ORM para almacenar una asignación confirmada."""
    grupo = models.ForeignKey(GrupoModel, on_delete=models.CASCADE, related_name='asignaciones')
    aula = models.ForeignKey('apps.academico.infrastructure.models.AulaModel', on_delete=models.SET_NULL, null=True)
    bloque_horario = models.ForeignKey(HorarioBloqueModel, on_delete=models.CASCADE, related_name='asignaciones')
    semestre = models.CharField(max_length=20)
    estado = models.CharField(max_length=50, default='CONFIRMADO')

    class Meta:
        # Asegurar que no haya dos asignaciones en el mismo slot/grupo
        unique_together = ('grupo', 'bloque_horario', 'semestre')

    def __str__(self):
        return f"Asignación {self.id} para Grupo {self.grupo.id}"


class ReglaNegocioModel(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    parametros = models.JSONField() # JSONB para parámetros dinámicos
    activa = models.BooleanField(default=True)

    class Meta:
        # Las reglas deben ser únicas por tipo y nombre
        unique_together = ('tipo', 'nombre')


class AulaModel(models.Model):
    """Modelo ORM para el recurso físico de aula."""
    nombre = models.CharField(max_length=255)
    capacidad = models.IntegerField()
    tipo = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True) # Estado general del aula
    restricciones = models.JSONField(blank=True, null=True)

class StrategyModel(models.Model):
    """Modelo para registrar y configurar estrategias de asignación."""
    nombre_estrategia = models.CharField(max_length=255, unique=True) # Ej: 'PrioridadEstudiantesStrategy'
    descripcion = models.TextField()
    parametros_default = models.JSONField()

# Nota: Se asume la existencia de modelos AulaModel y GrupoModel en apps.academico.infrastructure.models para que esto funcione.