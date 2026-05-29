from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("", lambda request: redirect("login"), name="home"),
    path(
        "login/",
        TemplateView.as_view(
            template_name="pages/login.html",
            extra_context={"recaptcha_site_key": settings.RECAPTCHA_PUBLIC_KEY},
        ),
        name="login",
    ),

    path(
        "dashboard/",
        TemplateView.as_view(
            template_name="pages/dashboard.html",
            extra_context={
                "solicitante": "Adriana Florez Cabal",
                "calendar_days": [
                    {"number": 1, "event": ""},
                    {"number": 2, "event": ""},
                    {"number": 3, "event": "Aula 204"},
                    {"number": 4, "event": ""},
                    {"number": 5, "event": "Lab Sistemas"},
                    {"number": 6, "event": ""},
                    {"number": 7, "event": ""},
                    {"number": 8, "event": ""},
                    {"number": 9, "event": "Bloque 3"},
                    {"number": 10, "event": ""},
                    {"number": 11, "event": ""},
                    {"number": 12, "event": "Aula 108"},
                    {"number": 13, "event": ""},
                    {"number": 14, "event": ""},
                    {"number": 15, "event": ""},
                    {"number": 16, "event": ""},
                    {"number": 17, "event": "Auditorio"},
                    {"number": 18, "event": ""},
                    {"number": 19, "event": ""},
                    {"number": 20, "event": "Sala 2"},
                    {"number": 21, "event": ""},
                    {"number": 22, "event": ""},
                    {"number": 23, "event": ""},
                    {"number": 24, "event": ""},
                    {"number": 25, "event": "Reserva"},
                    {"number": 26, "event": ""},
                    {"number": 27, "event": ""},
                    {"number": 28, "event": ""},
                    {"number": 29, "event": ""},
                    {"number": 30, "event": ""},
                ],
            },
        ),
        name="dashboard",
    ),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Compatibilidad con rutas usadas en el README/entrega
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui-legacy",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    path("api/", include("apps.usuarios.presentation.urls")),
    path("api/", include("apps.academico.presentation.urls")),

    path("api/", include("apps.asignacion.presentation.urls")),
    path("api/", include("apps.parametros.presentation.urls")),
    path("api/", include("apps.reservas.presentation.urls")),
    path("api/", include("apps.reportes.presentation.urls")),
    path("api/", include("apps.notificaciones.presentation.urls")),
    path("", include("django_prometheus.urls")),
]
