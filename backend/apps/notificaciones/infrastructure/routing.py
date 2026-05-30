from django.urls import path

from .consumers import (
    DisponibilidadAulaConsumer,
    NotificacionConsumer,
    ProgresoAsignacionConsumer,
)

websocket_urlpatterns = [
    path("ws/notificaciones/", NotificacionConsumer.as_asgi()),
    path("ws/notifications/", NotificacionConsumer.as_asgi()),
    path("ws/disponibilidad-aulas/", DisponibilidadAulaConsumer.as_asgi()),
    path("ws/asignacion/progreso/", ProgresoAsignacionConsumer.as_asgi()),
]
