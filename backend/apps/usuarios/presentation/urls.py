from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginConRecaptchaView, LoginView, UsuarioViewSet

router = DefaultRouter()
router.register(r"usuarios", UsuarioViewSet, basename="usuarios")

urlpatterns = [
    path("token/", LoginView.as_view(), name="token_obtain_pair"),
    path(
        "token/recaptcha/",
        LoginConRecaptchaView.as_view(),
        name="token_obtain_pair_recaptcha",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "usuarios/lista/",
        UsuarioViewSet.as_view({"get": "list"}),
        name="usuarios_lista",
    ),
    path(
        "usuarios/crear/",
        UsuarioViewSet.as_view({"post": "create"}),
        name="usuarios_crear",
    ),
    path(
        "usuarios/catalogo-roles/",
        UsuarioViewSet.as_view({"get": "roles", "post": "crear_rol"}),
        name="usuarios_roles_catalogo",
    ),
    path(
        "usuarios/roles/",
        UsuarioViewSet.as_view({"get": "roles", "post": "crear_rol"}),
        name="usuarios_roles",
    ),
    *router.urls,
]
