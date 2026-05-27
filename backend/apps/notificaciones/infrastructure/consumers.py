# backend/apps/notificaciones/infrastructure/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from systemserviciosdocentes.backend.apps.notificaciones.domain.entities import Notificacion
from sistemaserviciosdocentes.backend.apps.notificaciones.application.use_cases import NotificationService # Dependencia del caso de uso

class NotificacionConsumer(AsyncWebsocketConsumer):
    """
    Consumidor ASGI para manejar la conexión WebSocket, utilizado para
    actualizaciones en tiempo real (ej. nuevas notificaciones o cambios de estado).
    """

    # Se recomienda usar un canal específico y verificar permisos en el lado del servicio
    async def connect(self):
        # El user_id se pasa como parámetro de conexión (query params)
        self.user_id = self.scope['query_string']['user_id'].decode()
        if not self.user_id:
            await self.send(text_data=json.dumps({"error": "Debe proporcionar un 'user_id' para la conexión."}))
            await self.close()
            return

        self.room_group_name = f"notifications_{self.user_id}"
        await self.accept()
        await self.join(self.room_group_name)

    async def disconnect(self, close_code):
        # Asegurar que se deja el grupo de notificaciones al desconectar
        await self.leave_room(self.room_group_name)

    async def receive(self, text_data):
        """Maneja los mensajes entrantes (ej. 'GET_UNREAD', 'MARK_READ')."""
        try:
            data = json.loads(text_data)
            action = data.get("action")
            payload = data.get("payload", {})

            if action == "SUBSCRIBE_TO_NOTIFICATIONS":
                # El consumidor ya se unió al grupo, solo es informativo o para manejo futuro de suscripciones
                pass
            elif action == "GET_UNREAD_STATUS":
                await self.send(text_data=json.dumps({"status": "success", "message": "Enviando notificaciones no leídas..."}))
                # Aquí se debería llamar al caso de uso (NotificationService) para obtener los datos y enviarlos vía send()

            elif action == "ACKNOWLEDGE_READ":
                notif_id = payload.get("notification_id")
                await self.send(text_data=json.dumps({"status": "success", "message": f"Notificación {notif_id} marcada como leída."}))

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Payload JSON inválido"}))
        except Exception as e:
            print(f"Error en el consumidor de notificaciones: {e}")
            await self.send(text_data=json.dumps({"error": str(e)}))

    async def leave_room(self, room):
        """Lógica para dejar un grupo o sala."""
        pass # Implementado por canales-django generalmente
