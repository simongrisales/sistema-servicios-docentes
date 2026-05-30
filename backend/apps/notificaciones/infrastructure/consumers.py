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
                "tipo": "notification",
                "type": event.get("notification_type"),
                "title": event.get("title"),
                "message": event.get("message"),
                "unread_count": event.get("unread_count"),
            }
        )


class DisponibilidadAulaConsumer(AsyncJsonWebsocketConsumer):
    """Canal WebSocket publico para cambios de disponibilidad de aulas."""

    group_name = "disponibilidad_aulas"

    async def connect(self) -> None:
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code: int) -> None:
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def aula_actualizada(self, event: dict) -> None:
        await self.send_json(
            {
                "tipo": "aula_actualizada",
                "aula_id": event.get("aula_id"),
                "disponible": event.get("disponible"),
            }
        )


class ProgresoAsignacionConsumer(AsyncJsonWebsocketConsumer):
    """Canal WebSocket para progreso de procesos masivos de asignacion."""

    group_name = "progreso_asignacion"

    async def connect(self) -> None:
        user = self.scope.get("user")
        if user is None or not user.is_authenticated:
            await self.close(code=4401)
            return
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code: int) -> None:
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def progreso(self, event: dict) -> None:
        await self.send_json(
            {
                "tipo": "progreso",
                "porcentaje": event.get("porcentaje", 0),
                "grupos_procesados": event.get("grupos_procesados", 0),
            }
        )


class PanelSyncConsumer(AsyncJsonWebsocketConsumer):
    """Canal WebSocket autenticado para sincronizar dashboards en tiempo real."""

    group_name = "panel_sync"

    async def connect(self) -> None:
        user = self.scope.get("user")
        if user is None or not user.is_authenticated:
            await self.close(code=4401)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code: int) -> None:
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def catalogo_actualizado(self, event: dict) -> None:
        await self.send_json(
            {
                "tipo": "catalogo_actualizado",
                "entidad": event.get("entidad"),
                "accion": event.get("accion"),
                "detalle": event.get("detalle"),
                "payload": event.get("payload", {}),
            }
        )
