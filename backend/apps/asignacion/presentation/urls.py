from rest_framework.routers import DefaultRouter
from .views import AsignacionViewSet

router = DefaultRouter()

# Mapeo de las rutas REST para la asignación automática
router.register(r'asignacion', AsignacionViewSet, basename='asignacion')

urlpatterns = [
    # Nota: El router mapea automáticamente las acciones (list/create/etc.) a endpoints como /api/asignacion/.
]