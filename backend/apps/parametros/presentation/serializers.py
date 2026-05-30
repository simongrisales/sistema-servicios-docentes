"""Serializers de la app parametros."""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..domain.entities import GRUPOS_VALIDOS


class ParametroSerializer(serializers.Serializer):
    """Serializer de entrada/salida para CatalogoParametro."""

    clave = serializers.CharField(
        max_length=120,
        label=_("Clave"),
    )
    valor = serializers.JSONField(
        help_text=_("Valor estructurado: str, int, list o dict."),
        label=_("Valor"),
    )
    grupo = serializers.ChoiceField(
        choices=list(GRUPOS_VALIDOS),
        default="general",
        label=_("Grupo"),
    )
    descripcion = serializers.CharField(
        allow_blank=True,
        default="",
        required=False,
        label=_("Descripcion"),
    )
    activo = serializers.BooleanField(default=True, required=False, label=_("Activo"))


class ObtenerValorSerializer(serializers.Serializer):
    """Serializer para el endpoint de valor rapido."""

    clave = serializers.CharField(max_length=120, label=_("Clave"))
    default = serializers.JSONField(default=None, required=False, label=_("Valor por defecto"))
