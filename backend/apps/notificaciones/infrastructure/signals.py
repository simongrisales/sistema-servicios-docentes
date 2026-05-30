from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import NotificacionModel


@receiver(post_save, sender=NotificacionModel)
def broadcast_notification(sender, instance: NotificacionModel, created: bool, **kwargs):
    if not created:
        return

    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(
        f"notificaciones_usuario_{instance.usuario_destino_id}",
        {
            "type": "notification.message",
            "id": instance.notificacion_id,
            "notification_type": instance.tipo,
            "title": instance.titulo,
            "message": instance.mensaje,
        },
    )
