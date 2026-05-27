from rest_framework import serializers
from sistema_servicios_docentes.backend.apps.reservas.domain.dtos import CrearReservaInputDTO, ReservaOutputDTO # Asegurando que DTOs sean accesibles

class ReservaSerializer(serializers.ModelSerializer):
    """Serializador para manejar datos de reserva."""
    # Nota: Los campos FK deben ser serializados usando el modelo ORM real
    aula = serializers.PrimaryKeyRelatedField()
    bloque_horario = serializers.PrimaryKeyRelatedField()
    solicitante = serializers.SlugRelatedField(read_only=True)

    class Meta:
        # Se listan los campos del Modelo ORM (ReservaModel)
        model = 'apps.reservas.infrastructure.models.ReservaModel'
        fields = ['pk', 'aula', 'bloque_horario', 'solicitante', 'estado', 'fecha_creacion', 'fecha_expiracion']


class CrearReservaSerializer(serializers.Serializer):
    """Serializador de entrada para crear reservas, basado en el DTO."""
    aula_id = serializers.CharField()
    inicio = serializers.DateTimeField()
    fin = serializers.DateTimeField()
    solicitante_id = serializers.CharField()

class ReservaOutputSerializer(serializers.Serializer):
    """Serializa el resultado exitoso del proceso de reserva."""
    reserva_id = serializers.CharField()
    aula_id = serializers.CharField()
    inicio = serializers.DateTimeField()
    fin = serializers.DateTimeField()
    solicitante_id = serializers.CharField()
    estado = serializers.CharField()