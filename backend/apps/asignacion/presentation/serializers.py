from rest_framework import serializers
from asignacion.application.dtos import AsignacionOutputDTO, SimulacionOutputDTO

class SerializacionAsignacion(serializers.Serializer):
    # Campos para la solicitud de ejecución (POST /ejecutar)
    grupo_id = serializers.IntegerField()
    semestre = serializers.CharField()
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()

class SerializacionSimulacion(serializers.Serializer):
    # Campos para la solicitud de simulación (POST /simular)
    grupo_id = serializers.IntegerField()
    semestre = serializers.CharField()
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()

class SerializacionResultadoAsignacion(serializers.Serializer):
    # Campos para devolver el resultado de la asignación o simulación
    asignaciones_exitosas = serializers.ListField(child=serializers.DictField(), required=False)
    conflictos_encontrados = serializers.ListField(child=serializers.CharField())
    estado_generacion = serializers.CharField()

class SerializacionCoberturaOutput(serializers.Serializer):
    # Para el endpoint de verificación de cobertura total
    grupos_sin_aula = serializers.ListField(child=serializers.IntegerField(), required=False)
    grupo_ids_en_cobertura = serializers.ListField(child=serializers.IntegerField())