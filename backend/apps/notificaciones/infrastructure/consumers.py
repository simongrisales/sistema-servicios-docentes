from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificacionConsumer(AsyncJsonWebsocketConsumer):
    """Canal WebSocket para entregar notificaciones in-app por usuario."""

    async def connect(self) -> None:
        user = self.scope.get("user")
        if user is None or not user.is_authenticated:
            await self.close(code=4401)
            return

        self.group_name = f"notificaciones_usuario_{user.pk}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code: int) -> None:
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content: dict, **kwargs: object) -> None:
        if content.get("type") == "ping":
            await self.send_json({"type": "pong"})

    async def notification_message(self, event: dict) -> None:
        await self.send_json(
            {
                "id": event.get("id"),
                "type": event.get("notification_type"),
                "title": event.get("title"),
                "message": event.get("message"),
            }
        )
