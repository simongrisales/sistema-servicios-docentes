from rest_framework import serializers


class CrearReservaSerializer(serializers.Serializer):
    aula_id = serializers.CharField()
    inicio = serializers.DateTimeField()
    fin = serializers.DateTimeField()
    solicitante_id = serializers.CharField()


class ReservaOutputSerializer(serializers.Serializer):
    reserva_id = serializers.CharField()
    aula_id = serializers.CharField()
    aula_nombre = serializers.CharField(required=False)
    inicio = serializers.DateTimeField()
    fin = serializers.DateTimeField()
    solicitante_id = serializers.CharField()
    solicitante_nombre = serializers.CharField(required=False)
    estado = serializers.CharField()
