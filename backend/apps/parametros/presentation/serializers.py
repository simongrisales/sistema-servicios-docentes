"""Serializers de la app parametros."""

from rest_framework import serializers

from ..domain.entities import GRUPOS_VALIDOS


class ParametroSerializer(serializers.Serializer):
    """Serializer de entrada/salida para CatalogoParametro."""

    clave = serializers.CharField(max_length=120)
    valor = serializers.JSONField(
        help_text="Valor estructurado: str, int, list o dict."
    )
    grupo = serializers.ChoiceField(
        choices=list(GRUPOS_VALIDOS),
        default="general",
    )
    descripcion = serializers.CharField(
        allow_blank=True, default="", required=False
    )
    activo = serializers.BooleanField(default=True, required=False)


class ObtenerValorSerializer(serializers.Serializer):
    """Serializer para el endpoint de valor rápido."""

    clave = serializers.CharField(max_length=120)
    default = serializers.JSONField(default=None, required=False)
