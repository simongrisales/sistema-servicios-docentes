from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class SerializacionAsignacion(serializers.Serializer):
    grupo_id = serializers.CharField(label=_("Grupo"))
    aula_id = serializers.CharField(label=_("Aula"))
    bloque_horario_id = serializers.CharField(label=_("Bloque horario"))
    semestre = serializers.CharField(label=_("Semestre"))


class SerializacionSimulacion(serializers.Serializer):
    semestre = serializers.CharField(label=_("Semestre"))
    grupos = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list,
        label=_("Grupos"),
    )
    aulas = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list,
        label=_("Aulas"),
    )


class SerializacionResultadoAsignacion(serializers.Serializer):
    def to_representation(self, instance):
        if hasattr(instance, "exitoso"):
            return {
                "exitoso": instance.exitoso,
                "mensaje": instance.mensaje,
                "conflictos": getattr(instance, "conflictos", []),
                "asignaciones": getattr(instance, "asignaciones", []),
            }

        data = {
            "grupo_id": instance.grupo_id,
            "aula_id": instance.aula_id,
            "bloque_horario_id": instance.bloque_horario_id,
            "semestre": instance.semestre,
            "estado": instance.estado,
        }

        if getattr(instance, "mensaje", ""):
            data["mensaje"] = instance.mensaje
        if getattr(instance, "total_asignaciones", 0):
            data["total_asignaciones"] = instance.total_asignaciones
        if getattr(instance, "grupos_pendientes", 0):
            data["grupos_pendientes"] = instance.grupos_pendientes
        if getattr(instance, "conflictos", []):
            data["conflictos"] = instance.conflictos
        if getattr(instance, "asignaciones", []):
            data["asignaciones"] = instance.asignaciones
        return data


class SerializacionCoberturaOutput(serializers.Serializer):
    total_grupos = serializers.IntegerField(label=_("Total grupos"))
    grupos_con_aula = serializers.IntegerField(label=_("Grupos con aula"))
