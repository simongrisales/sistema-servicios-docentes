from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from django_prometheus.exports import ExportToDjangoView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.usuarios.presentation.views import (
    AdministradorDashboardView,
    AdmisionesDashboardView,
    AuxiliarDocDashboardView,
    DashboardRedirectView,
    FacultadDashboardView,
    LiderDocDashboardView,
    LoginPageView,
    LogoutView,
)

urlpatterns = [
    path("", lambda request: redirect("login"), name="home"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardRedirectView.as_view(), name="dashboard"),
    path(
        "dashboard/administrador/",
        AdministradorDashboardView.as_view(),
        name="dashboard_administrador",
    ),
    path(
        "dashboard/lider-doc/",
        LiderDocDashboardView.as_view(),
        name="dashboard_lider_doc",
    ),
    path(
        "dashboard/auxiliar-doc/",
        AuxiliarDocDashboardView.as_view(),
        name="dashboard_auxiliar_doc",
    ),
    path(
        "dashboard/facultad/",
        FacultadDashboardView.as_view(),
        name="dashboard_facultad",
    ),
    path(
        "dashboard/admisiones/",
        AdmisionesDashboardView.as_view(),
        name="dashboard_admisiones",
    ),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema")),
    path("api/", include("apps.usuarios.presentation.urls")),
    path("api/", include("apps.academico.presentation.urls")),
    path("api/", include("apps.asignacion.presentation.urls")),
    path("api/", include("apps.parametros.presentation.urls")),
    path("api/", include("apps.reservas.presentation.urls")),
    path("api/", include("apps.reportes.presentation.urls")),
    path("api/", include("apps.notificaciones.presentation.urls")),
    path("metrics/", ExportToDjangoView, name="prometheus-django-metrics"),
]
