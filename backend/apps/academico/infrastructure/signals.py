from __future__ import annotations

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.asignacion.infrastructure.tasks import recalculo_automatico_task

from .models import GrupoModel


@receiver(pre_save, sender=GrupoModel)
def _cache_previous_num_estudiantes(
    sender, instance: GrupoModel, **kwargs
) -> None:  # pragma: no cover - simple signal bridge
    if instance.pk is None:
        instance._previous_num_estudiantes = None
        return

    previous = sender.objects.filter(pk=instance.pk).values(
        "num_estudiantes",
        "semestre",
    ).first()
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
