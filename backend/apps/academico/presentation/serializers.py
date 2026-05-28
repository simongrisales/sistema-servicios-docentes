from rest_framework import serializers


class AulaInputSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=255)
    capacidad = serializers.IntegerField(min_value=1)
    tipo = serializers.CharField(max_length=100)
    disponible = serializers.BooleanField(default=True)


class AulaOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(allow_null=True)
    nombre = serializers.CharField()
    capacidad = serializers.IntegerField()
    tipo = serializers.CharField()
    disponible = serializers.BooleanField()


class GrupoSerializer(serializers.Serializer):
    curso_id = serializers.UUIDField()
    docente_id = serializers.UUIDField()
    codigo = serializers.CharField(max_length=50)
    num_estudiantes = serializers.IntegerField(min_value=0)
    semestre = serializers.CharField(max_length=20)
