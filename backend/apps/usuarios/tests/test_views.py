from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase

from apps.usuarios.infrastructure.models import RoleModel, RolSistema, UsuarioModel

ROLE_DASHBOARD_PATHS = {
    RolSistema.ADMINISTRADOR: "/dashboard/administrador/",
    RolSistema.LIDER_SD: "/dashboard/lider-doc/",
    RolSistema.AUXILIAR_SD: "/dashboard/auxiliar-doc/",
    RolSistema.FACULTAD: "/dashboard/facultad/",
    RolSistema.ADMISIONES: "/dashboard/admisiones/",
}


class UsuariosViewsTests(APITestCase):
    def _create_user(self, username: str, role_code: str):
        role, _ = RoleModel.objects.get_or_create(
            code=role_code,
            defaults={"name": role_code.title()},
        )
        UsuarioModel.objects.filter(username=username).delete()
        return UsuarioModel.objects.create_user(
            username=username,
            password="admin123",
            role=role,
        )

    def test_perfil_requiere_autenticacion(self):
        response = self.client.get("/api/usuarios/")
        assert response.status_code in {
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        }

    def test_usuario_autenticado_puede_listar_usuarios_y_roles(self):
        user = self._create_user("admin", RolSistema.ADMINISTRADOR)
        self.client.force_authenticate(user=user)

        usuarios = self.client.get("/api/usuarios/")
        roles = self.client.get("/api/usuarios/roles/")

        assert usuarios.status_code == status.HTTP_200_OK
        assert roles.status_code == status.HTTP_200_OK
        assert usuarios.data[0]["username"] == "admin"

    def test_login_web_redirige_al_dashboard_del_rol_y_crea_cookies(self):
        login_cases = [
            (RolSistema.ADMINISTRADOR, "admin", "/dashboard/administrador/"),
            (RolSistema.LIDER_SD, "lider", "/dashboard/lider-doc/"),
            (RolSistema.AUXILIAR_SD, "auxiliar", "/dashboard/auxiliar-doc/"),
            (RolSistema.FACULTAD, "facultad", "/dashboard/facultad/"),
            (RolSistema.ADMISIONES, "admisiones", "/dashboard/admisiones/"),
        ]

        for role_code, username, expected_url in login_cases:
            with self.subTest(role_code=role_code):
                self._create_user(username, role_code)

                response = self.client.post(
                    "/login/",
                    {
                        "username": username,
                        "password": "admin123",
                        "recaptcha_token": "",
                    },
                )

                assert response.status_code == status.HTTP_302_FOUND
                assert response.url == expected_url
                assert "access_token" in response.cookies
                assert "refresh_token" in response.cookies
                assert response.cookies["access_token"]["httponly"]
                assert response.cookies["refresh_token"]["httponly"]
                assert response.cookies["access_token"]["samesite"] == "Lax"
                assert response.cookies["refresh_token"]["samesite"] == "Lax"

    def test_login_web_muestra_error_con_credenciales_invalidas(self):
        response = self.client.post(
            "/login/",
            {
                "username": "nadie",
                "password": "mala",
                "recaptcha_token": "",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert "Credenciales invalidas" in response.content.decode()

    def test_token_jwt_exitoso_y_fallido(self):
        self._create_user("jwt_admin", RolSistema.ADMINISTRADOR)

        ok = self.client.post(
            "/api/token/",
            {"username": "jwt_admin", "password": "admin123"},
            format="json",
        )
        invalid = self.client.post(
            "/api/token/",
            {"username": "jwt_admin", "password": "mala"},
            format="json",
        )

        assert ok.status_code == status.HTTP_200_OK
        assert "access" in ok.data
        assert "refresh" in ok.data
        assert invalid.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_revoca_refresh_token_y_elimina_cookies(self):
        self._create_user("admin_logout", RolSistema.ADMINISTRADOR)

        login_response = self.client.post(
            "/login/",
            {
                "username": "admin_logout",
                "password": "admin123",
                "recaptcha_token": "",
            },
        )
        self.client.cookies["refresh_token"] = login_response.cookies[
            "refresh_token"
        ].value

        with patch(
            "apps.usuarios.presentation.views.RefreshToken.blacklist"
        ) as blacklist:
            response = self.client.get("/logout/")

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == "/login/"
        assert blacklist.called
        assert response.cookies["access_token"].value == ""
        assert response.cookies["refresh_token"].value == ""

    def test_refresh_token_queda_blacklisted_despues_del_logout(self):
        self._create_user("admin_blacklist", RolSistema.ADMINISTRADOR)

        login_response = self.client.post(
            "/login/",
            {
                "username": "admin_blacklist",
                "password": "admin123",
                "recaptcha_token": "",
            },
        )
        refresh_token = login_response.cookies["refresh_token"].value
        self.client.cookies["refresh_token"] = refresh_token

        self.client.get("/logout/")

        refresh_response = self.client.post(
            "/api/token/refresh/",
            {"refresh": refresh_token},
            format="json",
        )

        assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_dashboard_redirige_por_rol_y_bloquea_dashboard_ajeno(self):
        dashboard_cases = [
            (RolSistema.ADMINISTRADOR, "admin_dash"),
            (RolSistema.LIDER_SD, "lider_dash"),
            (RolSistema.AUXILIAR_SD, "auxiliar_dash"),
            (RolSistema.FACULTAD, "facultad_dash"),
            (RolSistema.ADMISIONES, "admisiones_dash"),
        ]

        for role_code, username in dashboard_cases:
            with self.subTest(role_code=role_code):
                user = self._create_user(username, role_code)
                self.client.force_login(user)

                response = self.client.get("/dashboard/")
                wrong_dashboard = (
                    "/dashboard/facultad/"
                    if role_code == RolSistema.ADMINISTRADOR
                    else "/dashboard/administrador/"
                )
                forbidden_dashboard = self.client.get(wrong_dashboard)

                assert response.status_code == status.HTTP_302_FOUND
                assert response.url == ROLE_DASHBOARD_PATHS[role_code]
                assert forbidden_dashboard.status_code == status.HTTP_302_FOUND
                assert forbidden_dashboard.url == ROLE_DASHBOARD_PATHS[role_code]

    def test_dashboard_muestra_cierre_de_sesion_visible(self):
        user = self._create_user("admin_nav", RolSistema.ADMINISTRADOR)
        self.client.force_login(user)

        response = self.client.get("/dashboard/administrador/")

        assert response.status_code == status.HTTP_200_OK
        assert "/logout/" in response.content.decode()
        assert "Cerrar sesion" in response.content.decode()
