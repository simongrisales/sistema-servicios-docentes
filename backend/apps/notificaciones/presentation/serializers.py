from rest_framework import serializers


class CrearNotificacionSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length=255)
    mensaje = serializers.CharField()
    tipo_notificacion = serializers.ChoiceField(
        choices=("conflict", "confirmation", "maintenance", "user_info")
    )
    usuario_destino_id = serializers.CharField()


class NotificacionOutputSerializer(serializers.Serializer):
    notificacion_id = serializers.CharField()
    titulo = serializers.CharField()
    mensaje = serializers.CharField()
    fecha_creacion = serializers.DateTimeField()
    tipo = serializers.CharField()
    es_leida = serializers.BooleanField()


class MarcarLeidaSerializer(serializers.Serializer):
    notificacion_id = serializers.CharField()
