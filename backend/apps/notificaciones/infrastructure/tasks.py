from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer


@shared_task(name="notificaciones.enviar_websocket")
def enviar_notificacion_websocket(
    user_id: str,
    notification_id: str,
    notification_type: str,
    title: str,
    message: str,
) -> None:
    """Publica una notificacion en el grupo WebSocket del usuario."""

    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(
        f"notificaciones_usuario_{user_id}",
        {
            "type": "notification.message",
            "id": notification_id,
            "notification_type": notification_type,
            "title": title,
            "message": message,
        },
    )
