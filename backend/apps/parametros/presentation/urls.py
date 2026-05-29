"""URLs de la app parametros."""

from rest_framework.routers import DefaultRouter

from .views import CatalogoParametroViewSet

router = DefaultRouter()
# lookup_field="clave" para que el pk en la URL sea la clave string
router.register(
    r"parametros",
    CatalogoParametroViewSet,
    basename="parametros",
)

urlpatterns = router.urls
