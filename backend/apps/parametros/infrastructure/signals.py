from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notificaciones.infrastructure.broadcasts import broadcast_panel_sync

from .models import CatalogoParametroModel


@receiver(post_save, sender=CatalogoParametroModel)
def broadcast_parametro_sync(
    sender, instance: CatalogoParametroModel, created: bool, **kwargs
) -> None:
    accion = "creado" if created else "actualizado"
    broadcast_panel_sync(
        entidad="parametros",
        accion=accion,
        detalle=f"Parametro {instance.clave} {accion}.",
        payload={
            "clave": instance.clave,
            "grupo": instance.grupo,
        },
    )
