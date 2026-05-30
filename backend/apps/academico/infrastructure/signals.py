from __future__ import annotations

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.asignacion.infrastructure.tasks import recalculo_automatico_task

from .models import AulaModel, GrupoModel


@receiver(pre_save, sender=GrupoModel)
def _cache_previous_num_estudiantes(
    sender, instance: GrupoModel, **kwargs
) -> None:  # pragma: no cover - simple signal bridge
    if instance.pk is None:
        instance._previous_num_estudiantes = None
        return

    previous = (
        sender.objects.filter(pk=instance.pk)
        .values(
            "num_estudiantes",
            "semestre",
        )
        .first()
    )
    instance._previous_num_estudiantes = (
        previous["num_estudiantes"] if previous else None
    )


@receiver(post_save, sender=GrupoModel)
def _enqueue_recalculo_por_cambio_de_matricula(
    sender, instance: GrupoModel, created: bool, **kwargs
) -> None:  # pragma: no cover - simple signal bridge
    previous_num_estudiantes = getattr(instance, "_previous_num_estudiantes", None)
    if created:
        return

    if previous_num_estudiantes is None:
        return

    if previous_num_estudiantes != instance.num_estudiantes:
        recalculo_automatico_task.delay(
            str(instance.pk),
            str(instance.semestre),
        )


@receiver(post_save, sender=AulaModel)
def _broadcast_disponibilidad_aula(
    sender, instance: AulaModel, **kwargs
) -> None:  # pragma: no cover - puente WebSocket
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(
        "disponibilidad_aulas",
        {
            "type": "aula.actualizada",
            "aula_id": str(instance.pk),
            "disponible": instance.disponible,
        },
    )
