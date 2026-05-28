from rest_framework.routers import DefaultRouter

from .views import ReporteViewSet

router = DefaultRouter()
router.register(r"reportes", ReporteViewSet, basename="reportes")

urlpatterns = router.urls
