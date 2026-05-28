from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import NotificacionesViewSet, campana_notificaciones

router = DefaultRouter()
router.register(
    r"notificaciones",
    NotificacionesViewSet,
    basename="notificaciones",
)

urlpatterns = [
    path(
        "notificaciones/campana/",
        campana_notificaciones,
        name="notificaciones-campana",
    ),
    *router.urls,
]
