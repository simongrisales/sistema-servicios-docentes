from django.db import models
# Usando el modelo de core para la base abstracta (asumido)
from core.models import BaseModel

class FacultadModel(BaseModel):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=255)

class ProgramaModel(BaseModel):
    facultad = models.ForeignKey(FacultadModel, on_delete=models.CASCADE, related_name='programas')
    nombre = models.CharField(max_length=255)
    programa_accreditado = models.BooleanField(default=False)

class DocenteModel(BaseModel):
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='docentes') # Relación con Django Auth
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    disponibilidad = models.TextField(blank=True, null=True)

class CursoModel(BaseModel):
    programa = models.ForeignKey(ProgramaModel, on_delete=models.CASCADE, related_name='cursos')
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    creditos = models.FloatField(default=3.0)

class AulaModel(BaseModel):
    nombre = models.CharField(max_length=255)
    capacidad = models.IntegerField()
    tipo = models.CharField(max_length=100) # Ej: Amfiteatro, Laboratorio
    disponible = models.BooleanField(default=True)
    restricciones = models.JSONField(blank=True, null=True)

class GrupoModel(BaseModel):
    curso = models.ForeignKey(CursoModel, on_delete=models.CASCADE, related_name='grupos')
    docente = models.ForeignKey(DocenteModel, on_delete=models.SET_NULL, null=True, related_name='grupos')
    num_estudiantes = models.IntegerField() # Campo crítico
    semestre = models.CharField(max_length=20)

class HorarioBloqueModel(BaseModel):
    dia = models.CharField(max_length=10) # Ej: Lunes
    hora_inicio = models.FloatField()  # Ejemplo de 8.5 para 8:30am
    hora_fin = models.FloatField()    # Ejemplo de 10.5 para 10:30am

class AsignacionModel(BaseModel):
    grupo = models.ForeignKey(GrupoModel, on_delete=models.CASCADE, related_name='asignaciones')
    aula = models.ForeignKey(AulaModel, on_delete=models.SET_NULL, null=True)
    bloque_horario = models.ForeignKey(HorarioBloqueModel, on_delete=models.CASCADE, related_name='asignaciones')
    semestre = models.CharField(max_length=20)
    estado = models.CharField(max_length=50, default='CONFIRMADO') # CONFIRMADO, RESERVADO, CANCELADO

class ReservaModel(BaseModel):
    aula = models.ForeignKey(AulaModel, on_delete=models.CASCADE, related_name='reservas')
    bloque_horario = models.ForeignKey(HorarioBloqueModel, on_delete=models.CASCADE)
    solicitante = models.CharField(max_length=255) # ID de usuario o nombre
    estado = models.CharField(max_length=50, default='PENDIENTE')
    fecha_expiracion = models.DateTimeField()

class ReglaNegocioModel(BaseModel):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100) # Ej: CAPACIDAD, DISPONIBILIDAD
    parametros = models.JSONField() # JSONB para parámetros dinámicos
    activa = models.BooleanField(default=True)

class CatalogoParametroModel(BaseModel):
    clave = models.CharField(max_length=100)
    valor = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

# Nota: Se asume la existencia de BaseRepository en core/repositories.py para heredar métodos CRUD básicos.