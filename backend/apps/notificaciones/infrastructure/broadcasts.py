from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_notification_created(
    user_id: str,
    notification_id: str,
    notification_type: str,
    title: str,
    message: str,
    unread_count: int | None = None,
) -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    payload = {
        "type": "notification.message",
        "id": notification_id,
        "notification_type": notification_type,
        "title": title,
        "message": message,
    }
    if unread_count is not None:
        payload["unread_count"] = unread_count

    try:
        async_to_sync(channel_layer.group_send)(
            f"notificaciones_usuario_{user_id}", payload
        )
    except Exception:
        return


def broadcast_panel_sync(
    entidad: str,
    accion: str,
    detalle: str = "",
    payload: dict | None = None,
) -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    try:
        async_to_sync(channel_layer.group_send)(
            "panel_sync",
            {
                "type": "catalogo.actualizado",
                "entidad": entidad,
                "accion": accion,
                "detalle": detalle,
                "payload": payload or {},
            },
        )
    except Exception:
        return
