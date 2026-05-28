from rest_framework.routers import DefaultRouter

from .views import AcademicoViewSet

router = DefaultRouter()
router.register(r"academico/aulas", AcademicoViewSet, basename="academico-aulas")

urlpatterns = router.urls
