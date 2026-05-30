from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class CrearNotificacionSerializer(serializers.Serializer):
    usuario_destino_id = serializers.CharField(label=_("Usuario destino"))
    titulo = serializers.CharField(label=_("Titulo"))
    mensaje = serializers.CharField(label=_("Mensaje"))
    tipo_notificacion = serializers.CharField(label=_("Tipo de notificacion"))


class MarcarLeidaSerializer(serializers.Serializer):
    notificacion_id = serializers.CharField(label=_("ID de notificacion"))


class NotificacionOutputSerializer(serializers.Serializer):
    notificacion_id = serializers.CharField(label=_("ID de notificacion"))
    titulo = serializers.CharField(label=_("Titulo"))
    mensaje = serializers.CharField(label=_("Mensaje"))
    fecha_creacion = serializers.DateTimeField(label=_("Fecha de creacion"))
    tipo = serializers.CharField(label=_("Tipo"))
    es_leida = serializers.BooleanField(label=_("Leida"))
