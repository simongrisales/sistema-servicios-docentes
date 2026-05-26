from rest_framework.routers import DefaultRouter
from .views import AcademicoViewSet

# Se inicializarán las rutas de la aplicación académico en el urls principal del proyecto.
router = DefaultRouter()
# Usamos un prefijo 'academico' para todas estas rutas
router.register(r'asignacion', AcademicoViewSet, basename='academico-viewset')

# Los endpoints básicos (listado, creación) se manejarán aquí o en el viewset principal.
urlpatterns = [
    # Rutas de gestión general: /api/academico/...
    path('asignacion/', include(router.urls))
]