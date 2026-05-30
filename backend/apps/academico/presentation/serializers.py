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


class GrupoSerializer(serializers.Serializer):
    curso_id = serializers.UUIDField(label=_("Curso"))
    docente_id = serializers.UUIDField(label=_("Docente"))
    codigo = serializers.CharField(max_length=50, label=_("Codigo"))
    num_estudiantes = serializers.IntegerField(
        min_value=0,
        label=_("Numero de estudiantes"),
    )
    semestre = serializers.CharField(max_length=20, label=_("Semestre"))
