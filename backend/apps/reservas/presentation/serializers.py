from rest_framework import serializers


class CrearReservaSerializer(serializers.Serializer):
    aula_id = serializers.CharField()
    inicio = serializers.DateTimeField()
    fin = serializers.DateTimeField()
    solicitante_id = serializers.CharField()


class ReservaOutputSerializer(serializers.Serializer):
    reserva_id = serializers.CharField()
    aula_id = serializers.CharField()
    inicio = serializers.DateTimeField()
    fin = serializers.DateTimeField()
    solicitante_id = serializers.CharField()
    estado = serializers.CharField()
