import uuid

from django.conf import settings
from django.db import models


class FacultadModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=255)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = "academico_facultad"


class ProgramaModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facultad = models.ForeignKey(
        FacultadModel,
        on_delete=models.CASCADE,
        related_name="programas",
    )
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "academico_programa"


class DocenteModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="docentes",
    )
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    disponibilidad = models.JSONField(default=dict, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "academico_docente"


class CursoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    programa = models.ForeignKey(
        ProgramaModel,
        on_delete=models.CASCADE,
        related_name="cursos",
    )
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    creditos = models.PositiveSmallIntegerField(default=3)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "academico_curso"


class AulaModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    capacidad = models.PositiveIntegerField()
    tipo = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    restricciones = models.JSONField(default=dict, blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = "academico_aula"


class GrupoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    curso = models.ForeignKey(
        CursoModel,
        on_delete=models.CASCADE,
        related_name="grupos",
    )
    docente = models.ForeignKey(
        DocenteModel,
        on_delete=models.PROTECT,
        related_name="grupos",
    )
    codigo = models.CharField(max_length=50)
    num_estudiantes = models.PositiveIntegerField()
    semestre = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "academico_grupo"
        unique_together = ("curso", "codigo", "semestre")


class HorarioBloqueModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dia = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "academico_horario_bloque"
