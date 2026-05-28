from django.urls import path

from .consumers import NotificacionConsumer

websocket_urlpatterns = [
    path("ws/notifications/", NotificacionConsumer.as_asgi()),
]
