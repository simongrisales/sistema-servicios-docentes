from django.db.models.signals import post_save
from django.dispatch import receiver

from .broadcasts import broadcast_notification_created
from .models import NotificacionModel


@receiver(post_save, sender=NotificacionModel)
def broadcast_notification(
    sender, instance: NotificacionModel, created: bool, **kwargs
):
    if not created:
        return
    unread_count = NotificacionModel.objects.filter(
        usuario_destino_id=instance.usuario_destino_id,
        es_leida=False,
        activo=True,
    ).count()

    broadcast_notification_created(
        str(instance.usuario_destino_id),
        instance.notificacion_id,
        instance.tipo,
        instance.titulo,
        instance.mensaje,
        unread_count,
    )
