from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class AulaInputSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=255, label=_("Nombre"))
    capacidad = serializers.IntegerField(min_value=1, label=_("Capacidad"))
    tipo = serializers.CharField(max_length=100, label=_("Tipo"))
    disponible = serializers.BooleanField(default=True, label=_("Disponible"))


class AulaOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(allow_null=True, label=_("ID"))
    nombre = serializers.CharField(label=_("Nombre"))
    capacidad = serializers.IntegerField(label=_("Capacidad"))
    tipo = serializers.CharField(label=_("Tipo"))
    disponible = serializers.BooleanField(label=_("Disponible"))
    activa = serializers.BooleanField(required=False, label=_("Activa"))


class AulaEstadoSerializer(serializers.Serializer):
    disponible = serializers.BooleanField(required=False, label=_("Disponible"))
    activa = serializers.BooleanField(required=False, label=_("Activa"))


class FacultadOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(label=_("ID"))
    codigo = serializers.CharField(label=_("Codigo"))
    nombre = serializers.CharField(label=_("Nombre"))
    activa = serializers.BooleanField(label=_("Activa"))
    programas = serializers.IntegerField(label=_("Programas"))


class ProgramaOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(label=_("ID"))
    facultad_id = serializers.UUIDField(label=_("Facultad"))
    facultad_codigo = serializers.CharField(label=_("Codigo de facultad"))
    facultad_nombre = serializers.CharField(label=_("Facultad"))
    codigo = serializers.CharField(label=_("Codigo"))
    nombre = serializers.CharField(label=_("Nombre"))
    activo = serializers.BooleanField(label=_("Activo"))


class DocenteOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(label=_("ID"))
    nombre = serializers.CharField(label=_("Nombre"))
    email = serializers.EmailField(label=_("Correo electronico"))
    activo = serializers.BooleanField(label=_("Activo"))


class CursoOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(label=_("ID"))
    programa_id = serializers.UUIDField(label=_("Programa"))
    programa_nombre = serializers.CharField(required=False, label=_("Programa"))
    facultad_nombre = serializers.CharField(required=False, label=_("Facultad"))
    codigo = serializers.CharField(label=_("Codigo"))
    nombre = serializers.CharField(label=_("Nombre"))
    creditos = serializers.IntegerField(label=_("Creditos"))
    activo = serializers.BooleanField(label=_("Activo"))


class GrupoOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(label=_("ID"))
    curso_id = serializers.UUIDField(label=_("Curso"))
    curso_codigo = serializers.CharField(required=False, label=_("Codigo del curso"))
    curso_nombre = serializers.CharField(required=False, label=_("Curso"))
    docente_id = serializers.UUIDField(label=_("Docente"))
    docente_nombre = serializers.CharField(required=False, label=_("Docente"))
    codigo = serializers.CharField(label=_("Codigo"))
    num_estudiantes = serializers.IntegerField(label=_("Numero de estudiantes"))
    semestre = serializers.CharField(label=_("Semestre"))
    activo = serializers.BooleanField(label=_("Activo"))


class GrupoSerializer(serializers.Serializer):
    curso_id = serializers.UUIDField(label=_("Curso"))
    docente_id = serializers.UUIDField(label=_("Docente"))
    codigo = serializers.CharField(max_length=50, label=_("Codigo"))
    num_estudiantes = serializers.IntegerField(
        min_value=0,
        label=_("Numero de estudiantes"),
    )
    semestre = serializers.CharField(max_length=20, label=_("Semestre"))


class AulaBusquedaSerializer(serializers.Serializer):
    q = serializers.CharField(required=False, allow_blank=True, label=_("Busqueda"))
