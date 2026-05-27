# reservas/presentation/urls.py

from django.urls import apirouter
from rest_framework.routers import DefaultRouter
from .views import ReservasViewSet

router = DefaultRouter()
# Ruta base para todas las operaciones CRUD (GET, POST) en /api/reservas/
router.register(r'reservas', ReservasViewSet, basename='reserva')

# Exponemos acciones personalizadas de negocio que no son parte del CRUD estándar:
urlpatterns = [
    # Endpoint para confirmar una reserva específica por ID
    path('reservas/<str:pk>/confirm/', ReservasViewSet.as_view({'post': 'confirm'}), name='reserva-confirmar'),
    # Endpoint para cancelar una reserva específica por ID
    path('reservas/<str:pk>/cancel/', ReservasViewSet.as_view({'post': 'cancel'}), name='reserva-cancelar'),
]