from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.notificaciones.infrastructure.broadcasts import broadcast_panel_sync

from .models import AsignacionModel


@receiver(post_save, sender=AsignacionModel)
def broadcast_asignacion_sync(
    sender, instance: AsignacionModel, created: bool, **kwargs
) -> None:
    accion = "creada" if created else "actualizada"
    broadcast_panel_sync(
        entidad="asignaciones",
        accion=accion,
        detalle=f"Asignacion de {instance.grupo_id} {accion}.",
        payload={
            "grupo_id": str(instance.grupo_id),
            "aula_id": str(instance.aula_id),
            "semestre": instance.semestre,
        },
    )


@receiver(post_delete, sender=AsignacionModel)
def broadcast_asignacion_eliminada(sender, instance: AsignacionModel, **kwargs) -> None:
    broadcast_panel_sync(
        entidad="asignaciones",
        accion="eliminada",
        detalle=f"Asignacion de {instance.grupo_id} eliminada.",
        payload={
            "grupo_id": str(instance.grupo_id),
            "aula_id": str(instance.aula_id),
            "semestre": instance.semestre,
        },
    )
