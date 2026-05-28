from rest_framework.routers import DefaultRouter

from .views import ReservasViewSet

router = DefaultRouter()
router.register(r"reservas", ReservasViewSet, basename="reservas")

urlpatterns = router.urls
