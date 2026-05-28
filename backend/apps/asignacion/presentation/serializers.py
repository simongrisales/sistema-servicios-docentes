from rest_framework import serializers


class SerializacionAsignacion(serializers.Serializer):
    grupo_id = serializers.CharField()
    aula_id = serializers.CharField()
    bloque_horario_id = serializers.CharField()
    semestre = serializers.CharField(max_length=20)


class SerializacionSimulacion(serializers.Serializer):
    semestre = serializers.CharField(max_length=20)
    grupos = serializers.ListField(child=serializers.DictField(), required=False)
    aulas = serializers.ListField(child=serializers.DictField(), required=False)


class SerializacionResultadoAsignacion(serializers.Serializer):
    grupo_id = serializers.CharField(required=False)
    aula_id = serializers.CharField(required=False)
    bloque_horario_id = serializers.CharField(required=False)
    semestre = serializers.CharField(required=False)
    estado = serializers.CharField(required=False)
    exitoso = serializers.BooleanField(required=False)
    mensaje = serializers.CharField(required=False)
    conflictos = serializers.ListField(
        child=serializers.CharField(),
        required=False,
    )


class SerializacionCoberturaOutput(serializers.Serializer):
    total_grupos = serializers.IntegerField()
    grupos_con_aula = serializers.IntegerField()
