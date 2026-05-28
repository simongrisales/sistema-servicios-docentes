from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/", include("apps.usuarios.presentation.urls")),
    path("api/", include("apps.academico.presentation.urls")),
    path("api/", include("apps.asignacion.presentation.urls")),
    path("api/", include("apps.reservas.presentation.urls")),
    path("api/", include("apps.reportes.presentation.urls")),
    path("api/", include("apps.notificaciones.presentation.urls")),
    path("", include("django_prometheus.urls")),
]
