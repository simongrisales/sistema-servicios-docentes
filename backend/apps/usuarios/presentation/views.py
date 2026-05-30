from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView, TemplateView
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV3
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.notificaciones.infrastructure.models import NotificacionModel

from ..application.dtos import UsuarioInputDTO
from ..application.use_cases import CrearUsuario, ListarRoles, ListarUsuarios
from ..infrastructure.models import RoleModel
from ..infrastructure.permissions import EsAdministrador
from ..infrastructure.repositories import UsuariosRepository
from .serializers import RolInputSerializer, RolSerializer, UsuarioSerializer

ROLE_DASHBOARD_URLS = {
    "administrador": "dashboard_administrador",
    "lider_sd": "dashboard_lider_doc",
    "lider_doc": "dashboard_lider_doc",
    "auxiliar_sd": "dashboard_auxiliar_doc",
    "auxiliar_doc": "dashboard_auxiliar_doc",
    "facultad": "dashboard_facultad",
    "admisiones": "dashboard_admisiones",
}

ROLE_LABELS = {
    "administrador": _("Administrador"),
    "lider_sd": _("Lider DOC"),
    "auxiliar_sd": _("Auxiliar DOC"),
    "facultad": _("Facultad"),
    "admisiones": _("Admisiones"),
}


def dashboard_name_for_role(role_code: str | None) -> str:
    return ROLE_DASHBOARD_URLS.get((role_code or "").lower(), "dashboard_administrador")


def dashboard_label_for_role(role_code: str | None) -> str:
    return ROLE_LABELS.get((role_code or "").lower(), _("Administrador"))


def _validate_recaptcha_or_raise(token: str, widget_factory) -> None:
    if not token:
        raise ValueError(_("Completa el captcha antes de ingresar."))

    if settings.RECAPTCHA_TESTING_MODE and token.upper() == "PASSED":
        return

    field = ReCaptchaField(widget=widget_factory())
    try:
        field.clean(token)
    except ValidationError as exc:
        message = (
            exc.messages[0]
            if getattr(exc, "messages", None)
            else _("Captcha invalido.")
        )
        raise ValueError(message) from exc


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class LoginPageView(TemplateView):
    template_name = "usuarios/login.html"

    def _captcha_widget(self):
        if settings.DEBUG:
            return ReCaptchaV2Checkbox()
        return ReCaptchaV3(action="login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recaptcha_site_key"] = settings.RECAPTCHA_PUBLIC_KEY
        context["recaptcha_mode"] = "v2" if settings.DEBUG else "v3"
        return context

    def post(self, request, *args, **kwargs):
        recaptcha_token = request.POST.get("recaptcha_token", "") or request.POST.get(
            "g-recaptcha-response", ""
        )
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        try:
            _validate_recaptcha_or_raise(recaptcha_token, self._captcha_widget)
        except ValueError as exc:
            return self.render_to_response(
                self.get_context_data(error_message=str(exc))
            )

        user = authenticate(request, username=username, password=password)
        if user is None:
            return self.render_to_response(
                self.get_context_data(error_message=_("Credenciales invalidas."))
            )

        login(request, user)
        refresh = RefreshToken.for_user(user)
        response = redirect(dashboard_name_for_role(getattr(user, "role_code", "")))
        response.set_cookie(
            "access_token",
            str(refresh.access_token),
            httponly=True,
            secure=not settings.DEBUG,
            samesite="Lax",
        )
        response.set_cookie(
            "refresh_token",
            str(refresh),
            httponly=True,
            secure=not settings.DEBUG,
            samesite="Lax",
        )
        return response


class LogoutView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = "login"

    def get(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError:
                pass
        logout(request)
        response = super().get(request, *args, **kwargs)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class LoginConRecaptchaView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Valida recaptcha_token cuando aplica y luego autentica con simplejwt."""
        recaptcha_token = request.data.get("recaptcha_token", "") or request.data.get(
            "g-recaptcha-response", ""
        )

        try:
            _validate_recaptcha_or_raise(
                recaptcha_token,
                lambda: (
                    ReCaptchaV2Checkbox()
                    if settings.DEBUG
                    else ReCaptchaV3(action="login")
                ),
            )
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().post(request, *args, **kwargs)


class UsuarioViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _repo(self) -> UsuariosRepository:
        return UsuariosRepository()

    def list(self, request):
        usuarios = ListarUsuarios(self._repo()).execute()
        return Response(UsuarioSerializer(usuarios, many=True).data)

    def create(self, request):
        serializer = UsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = CrearUsuario(self._repo()).execute(
            UsuarioInputDTO(**serializer.validated_data)
        )
        return Response(
            UsuarioSerializer(usuario).data,
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        usuario = self._repo().find_by_id(pk)
        if usuario is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(UsuarioSerializer(usuario).data)

    @action(detail=False, methods=["get"], url_path="roles")
    def roles(self, request):
        roles = ListarRoles(self._repo()).execute()
        return Response(RolSerializer(roles, many=True).data)

    @action(detail=False, methods=["post"], url_path="roles")
    def crear_rol(self, request):
        if not EsAdministrador().has_permission(request, self):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = RolInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role, _ = RoleModel.objects.update_or_create(
            code=serializer.validated_data["code"],
            defaults={
                "name": serializer.validated_data["name"],
                "description": serializer.validated_data.get("description", ""),
            },
        )
        payload = {
            "role_id": role.id,
            "code": role.code or "",
            "name": role.name,
            "description": role.description,
        }
        return Response(payload, status=status.HTTP_201_CREATED)


class BaseDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "pages/dashboard.html"
    required_role_code: str | None = None
    dashboard_url_name = "dashboard_administrador"
    page_title = _("Dashboard")
    dashboard_brand = _("Sistema de Servicios Docentes")
    dashboard_description = _("Panel de operacion academica UCO")
    sidebar_items: list[dict[str, str]] = []
    stats_cards: list[dict[str, str]] = []
    highlights: list[dict[str, str]] = []
    recent_rows: list[dict[str, str]] = []
    quick_actions: list[dict[str, str]] = []
    support_notes: list[str] = []

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            current_role = (getattr(request.user, "role_code", "") or "").lower()
            if (
                self.required_role_code
                and current_role
                and current_role != self.required_role_code
            ):
                return redirect(dashboard_name_for_role(current_role))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_role = (getattr(self.request.user, "role_code", "") or "").lower()
        primary_anchor_by_role = {
            "administrador": "#admin-logs",
            "lider_sd": "#leader-reportes",
            "lider_doc": "#leader-reportes",
            "auxiliar_sd": "#aux-reservas",
            "auxiliar_doc": "#aux-reservas",
            "facultad": "#faculty-grupos",
            "admisiones": "#admissions-validacion",
        }
        notifications_count = 0
        notifications_list = []
        if getattr(self.request.user, "is_authenticated", False):
            notifications_qs = NotificacionModel.objects.filter(
                usuario_destino_id=self.request.user.id,
                es_leida=False,
                activo=True,
            ).order_by("-fecha_creacion")
            notifications_count = notifications_qs.count()
            notifications_list = [
                {
                    "id": notification.notificacion_id,
                    "titulo": notification.titulo,
                    "mensaje": notification.mensaje,
                    "tipo": notification.tipo,
                    "fecha_creacion": notification.fecha_creacion,
                }
                for notification in notifications_qs[:8]
            ]
        show_metrics = user_role == "administrador"
        context.update(
            {
                "page_title": self.page_title,
                "dashboard_brand": self.dashboard_brand,
                "dashboard_description": self.dashboard_description,
                "dashboard_url_name": self.dashboard_url_name,
                "dashboard_role_code": user_role,
                "dashboard_role_label": dashboard_label_for_role(user_role),
                "dashboard_user_id": getattr(self.request.user, "id", ""),
                "dashboard_sidebar_items": self.sidebar_items,
                "dashboard_notifications_count": notifications_count,
                "dashboard_notifications": notifications_list,
                "dashboard_primary_anchor": primary_anchor_by_role.get(
                    user_role, "#main-app"
                ),
                "dashboard_show_metrics": show_metrics,
                "grafana_url": (
                    f"http://localhost:{settings.GRAFANA_PORT}" if show_metrics else ""
                ),
                "prometheus_url": (
                    f"http://localhost:{settings.PROMETHEUS_PORT}"
                    if show_metrics
                    else ""
                ),
                "stats_cards": self.stats_cards,
                "highlights": self.highlights,
                "recent_rows": self.recent_rows,
                "quick_actions": self.quick_actions,
                "support_notes": self.support_notes,
            }
        )
        return context


class DashboardRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        role_code = (getattr(self.request.user, "role_code", "") or "").lower()
        return reverse(dashboard_name_for_role(role_code))


class AdministradorDashboardView(BaseDashboardView):
    template_name = "pages/dashboard_administrador.html"
    required_role_code = "administrador"
    dashboard_url_name = "dashboard_administrador"
    page_title = _("Dashboard Administrador")
    dashboard_description = _("Centro de control institucional")
    sidebar_items = [
        {
            "label": _("Gestion de usuarios"),
            "href": "#admin-usuarios",
            "icon": "users",
        },
        {
            "label": _("Catalogo de parametros"),
            "href": "#admin-parametros",
            "icon": "settings",
        },
        {
            "label": _("Logs centralizados"),
            "href": "#admin-logs",
            "icon": "logs",
        },
        {
            "label": _("Metricas del sistema"),
            "href": "#admin-metricas",
            "icon": "metrics",
        },
    ]
    stats_cards = [
        {
            "label": _("Aulas registradas"),
            "value": "48",
            "detail": _("Infraestructura activa"),
        },
        {
            "label": _("Grupos cargados"),
            "value": "126",
            "detail": _("Semestre vigente"),
        },
        {
            "label": _("Usuarios activos"),
            "value": "34",
            "detail": _("Acceso con rol validado"),
        },
        {
            "label": _("Alertas abiertas"),
            "value": "7",
            "detail": _("Requieren revision"),
        },
    ]
    highlights = [
        {
            "title": _("Gestion de usuarios"),
            "text": _(
                "Crear, editar y asignar roles institucionales con control de acceso."
            ),
        },
        {
            "title": _("Catalogo de parametros"),
            "text": _(
                "Configurar reglas del sistema y parametros de negocio sin tocar codigo."
            ),
        },
        {
            "title": _("Logs centralizados"),
            "text": _(
                "Supervisar eventos, errores y trazas de operacion en menos de un minuto."
            ),
        },
        {
            "title": _("Grafana y Prometheus"),
            "text": _(
                "Acceso directo a metricas y alertas de observabilidad del stack local."
            ),
        },
    ]
    recent_rows = [
        {
            "first": "usuarios",
            "second": _("Alta de usuario lider_doc"),
            "third": _("Hace 4 min"),
        },
        {
            "first": "parametros",
            "second": _("Regla de capacidad maxima actualizada"),
            "third": _("Hace 17 min"),
        },
        {
            "first": "logs",
            "second": _("Sincronizacion de catalogos completada"),
            "third": _("Hace 31 min"),
        },
    ]
    quick_actions = [
        {"label": _("Abrir usuarios"), "href": "#admin-usuarios"},
        {"label": _("Abrir parametros"), "href": "#admin-parametros"},
        {
            "label": _("Ver Grafana"),
            "href": f"http://localhost:{settings.GRAFANA_PORT}",
        },
        {
            "label": _("Ver Prometheus"),
            "href": f"http://localhost:{settings.PROMETHEUS_PORT}",
        },
    ]
    support_notes = [
        _(
            "Los ultimos eventos del sistema deben revisarse antes del inicio de semestre."
        ),
        _(
            "El catalogo de parametros controla las reglas institucionales de asignacion."
        ),
    ]


class LiderDocDashboardView(BaseDashboardView):
    template_name = "pages/dashboard_lider_doc.html"
    required_role_code = "lider_sd"
    dashboard_url_name = "dashboard_lider_doc"
    page_title = _("Dashboard Lider DOC")
    dashboard_description = _("Ejecucion y supervision de la asignacion automatica")
    sidebar_items = [
        {
            "label": _("Ejecutar asignacion"),
            "href": "#leader-asignacion",
            "icon": "play",
        },
        {"label": _("Simulacion"), "href": "#leader-simulacion", "icon": "beaker"},
        {"label": _("Cobertura"), "href": "#leader-cobertura", "icon": "chart"},
        {"label": _("Reportes"), "href": "#leader-reportes", "icon": "report"},
    ]
    stats_cards = [
        {
            "label": _("Grupos cubiertos"),
            "value": "118",
            "detail": _("92% de cobertura"),
        },
        {
            "label": _("Grupos pendientes"),
            "value": "10",
            "detail": _("Sin aula asignada"),
        },
        {
            "label": _("Conflictos"),
            "value": "2",
            "detail": _("Revisar cruces detectados"),
        },
        {
            "label": _("Estado proceso"),
            "value": _("Activo"),
            "detail": _("Ultima corrida hace 8 min"),
        },
    ]
    highlights = [
        {
            "title": _("Asignacion automatica"),
            "text": _(
                "Proceso principal con confirmacion y seguimiento en tiempo real."
            ),
        },
        {
            "title": _("Simulacion de escenarios"),
            "text": _("Probar combinaciones sin persistir cambios en base de datos."),
        },
        {
            "title": _("Cobertura total"),
            "text": _(
                "Validar que todos los grupos queden atendidos antes de publicar."
            ),
        },
        {
            "title": _("Reportes operativos"),
            "text": _("Exportar resumenes de ocupacion y conflictos detectados."),
        },
    ]
    recent_rows = [
        {
            "first": "grupo 3A",
            "second": _("Asignado a Aula 204"),
            "third": _("Correcto"),
        },
        {
            "first": "grupo 2B",
            "second": _("Pendiente por capacidad"),
            "third": _("Revisar"),
        },
        {
            "first": "grupo 4C",
            "second": _("Simulacion exitosa"),
            "third": _("Sin cambios"),
        },
    ]
    quick_actions = [
        {"label": _("Ejecutar asignacion"), "href": "#leader-asignacion"},
        {"label": _("Ejecutar simulacion"), "href": "#leader-simulacion"},
        {"label": _("Ver reportes"), "href": "#leader-reportes"},
    ]
    support_notes = [
        _(
            "El boton principal debe usar confirmacion antes de ejecutar la asignacion real."
        ),
        _(
            "La barra de progreso se actualiza en tiempo real con los eventos del proceso."
        ),
    ]


class AuxiliarDocDashboardView(BaseDashboardView):
    template_name = "pages/dashboard_auxiliar_doc.html"
    required_role_code = "auxiliar_sd"
    dashboard_url_name = "dashboard_auxiliar_doc"
    page_title = _("Dashboard Auxiliar DOC")
    dashboard_description = _("Gestion parcial de asignaciones y reservas temporales")
    sidebar_items = [
        {
            "label": _("Asignaciones parciales"),
            "href": "#aux-asignaciones",
            "icon": "edit",
        },
        {
            "label": _("Calendario semanal"),
            "href": "#aux-calendario",
            "icon": "calendar",
        },
        {
            "label": _("Reservas activas"),
            "href": "#aux-reservas",
            "icon": "clock",
        },
        {
            "label": _("Buscador de aulas"),
            "href": "#aux-buscador",
            "icon": "search",
        },
    ]
    stats_cards = [
        {
            "label": _("Asignaciones del dia"),
            "value": "14",
            "detail": _("Tiempo parcial gestionado"),
        },
        {
            "label": _("Reservas activas"),
            "value": "6",
            "detail": _("Con expiracion controlada"),
        },
        {
            "label": _("Aulas libres"),
            "value": "19",
            "detail": _("Disponibilidad inmediata"),
        },
        {
            "label": _("Conflictos resueltos"),
            "value": "3",
            "detail": _("Sin duplicidad de horario"),
        },
    ]
    highlights = [
        {
            "title": _("Asignaciones parciales"),
            "text": _("Crear, editar y eliminar registros de forma rapida."),
        },
        {
            "title": _("Calendario semanal"),
            "text": _("Visualizar la semana operativa con tareas y reservas."),
        },
        {
            "title": _("Reservas temporales"),
            "text": _("Monitorear cupos activos y su expiracion en tiempo util."),
        },
        {
            "title": _("Buscador de aulas"),
            "text": _("Filtrar por horario, capacidad y tipo de espacio."),
        },
    ]
    recent_rows = [
        {
            "first": "Aula 108",
            "second": _("Disponible 10:00 - 12:00"),
            "third": _("Capacidad 35"),
        },
        {
            "first": "Aula 204",
            "second": _("Reserva activa hasta 14:00"),
            "third": _("Pendiente"),
        },
        {
            "first": "Sala 2",
            "second": _("Asignacion parcial actualizada"),
            "third": _("OK"),
        },
    ]
    quick_actions = [
        {"label": _("Nueva asignacion"), "href": "#aux-asignaciones"},
        {"label": _("Nueva reserva"), "href": "#aux-reservas"},
        {"label": _("Buscar aula"), "href": "#aux-buscador"},
    ]
    support_notes = [
        _("El auxiliar debe ver solo operaciones parciales y reservas temporales."),
        _("La busqueda de aulas se refresca en tiempo real al cambiar disponibilidad."),
    ]


class FacultadDashboardView(BaseDashboardView):
    template_name = "pages/dashboard_facultad.html"
    required_role_code = "facultad"
    dashboard_url_name = "dashboard_facultad"
    page_title = _("Dashboard Facultad")
    dashboard_description = _("Ingreso de grupos y seguimiento de asignacion")
    sidebar_items = [
        {
            "label": _("Ingresar grupo"),
            "href": "#faculty-grupo",
            "icon": "form",
        },
        {
            "label": _("Grupos ingresados"),
            "href": "#faculty-grupos",
            "icon": "list",
        },
        {
            "label": _("Disponibilidad"),
            "href": "#faculty-disponibilidad",
            "icon": "signal",
        },
        {
            "label": _("Consulta de aula"),
            "href": "#faculty-consulta",
            "icon": "search",
        },
    ]
    stats_cards = [
        {
            "label": _("Grupos ingresados"),
            "value": "41",
            "detail": _("Esperando validacion"),
        },
        {
            "label": _("Grupos asignados"),
            "value": "33",
            "detail": _("Con aula definida"),
        },
        {
            "label": _("Aulas disponibles"),
            "value": "18",
            "detail": _("Actualizacion en vivo"),
        },
        {"label": _("Alertas"), "value": "4", "detail": _("Datos pendientes")},
    ]
    highlights = [
        {
            "title": _("Ingreso de grupo"),
            "text": _("Materia, docente, horario y cupo por grupo de la facultad."),
        },
        {
            "title": _("Estado de asignacion"),
            "text": _("Cada grupo muestra si ya fue asignado o sigue pendiente."),
        },
        {
            "title": _("Disponibilidad en vivo"),
            "text": _("Indicador conectado al estado de aulas por WebSocket."),
        },
        {
            "title": _("Consulta de aula"),
            "text": _("Ver rapidamente que aula fue asignada a cada grupo."),
        },
    ]
    recent_rows = [
        {"first": "Calculo I", "second": _("Grupo 1A"), "third": _("Pendiente")},
        {"first": "Algoritmos", "second": _("Grupo 2B"), "third": _("Asignado")},
        {"first": "Bases de datos", "second": _("Grupo 3C"), "third": _("Validado")},
    ]
    quick_actions = [
        {"label": _("Nuevo grupo"), "href": "#faculty-grupo"},
        {"label": _("Consultar aula"), "href": "#faculty-consulta"},
        {"label": _("Actualizar disponibilidad"), "href": "#faculty-disponibilidad"},
    ]
    support_notes = [
        _("Los datos ingresados por la facultad alimentan la asignacion automatica."),
        _("El estado de aula debe refrescarse sin recargar la pagina."),
    ]


class AdmisionesDashboardView(BaseDashboardView):
    template_name = "pages/dashboard_admisiones.html"
    required_role_code = "admisiones"
    dashboard_url_name = "dashboard_admisiones"
    page_title = _("Dashboard Admisiones")
    dashboard_description = _("Carga masiva de grupos y seguimiento de validacion")
    sidebar_items = [
        {
            "label": _("Carga masiva"),
            "href": "#admissions-carga",
            "icon": "upload",
        },
        {
            "label": _("Progreso"),
            "href": "#admissions-cobertura",
            "icon": "progress",
        },
        {"label": _("Validacion"), "href": "#admissions-validacion", "icon": "check"},
        {"label": _("Cobertura"), "href": "#admissions-cobertura", "icon": "report"},
    ]
    stats_cards = [
        {
            "label": _("Grupos cargados"),
            "value": "52",
            "detail": _("Carga masiva activa"),
        },
        {"label": _("Procesados"), "value": "47", "detail": _("Validacion completa")},
        {"label": _("Errores"), "value": "5", "detail": _("Requieren correccion")},
        {"label": _("Cobertura"), "value": "90%", "detail": _("Progreso del lote")},
    ]
    highlights = [
        {
            "title": _("Carga masiva"),
            "text": _("Ingresar grupos con numero de estudiantes en un solo flujo."),
        },
        {
            "title": _("Progreso en tiempo real"),
            "text": _("Mostrar avance del lote con Celery y WebSocket."),
        },
        {
            "title": _("Tabla de validacion"),
            "text": _("Listar grupos con su estado y observaciones de control."),
        },
        {
            "title": _("Reportes de cobertura"),
            "text": _("Consultar si la carga quedo lista para la asignacion."),
        },
    ]
    recent_rows = [
        {"first": "Grupo 1A", "second": _("Validado"), "third": _("35 estudiantes")},
        {"first": "Grupo 2B", "second": _("En proceso"), "third": _("22 estudiantes")},
        {"first": "Grupo 3C", "second": _("Con error"), "third": _("Campo faltante")},
    ]
    quick_actions = [
        {"label": _("Cargar archivo"), "href": "#admissions-carga"},
        {"label": _("Ver progreso"), "href": "#admissions-cobertura"},
        {"label": _("Reporte de cobertura"), "href": "#admissions-cobertura"},
    ]
    support_notes = [
        _("Admisiones solo ingresa la cantidad real de estudiantes por grupo."),
        _("La barra de progreso se sincroniza con el worker Celery en tiempo real."),
    ]
