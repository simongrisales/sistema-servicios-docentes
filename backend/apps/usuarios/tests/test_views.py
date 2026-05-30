from rest_framework import status
from rest_framework.test import APITestCase

from apps.usuarios.infrastructure.models import RoleModel, RolSistema, UsuarioModel


class UsuariosViewsTests(APITestCase):
    def test_perfil_requiere_autenticacion(self):
        response = self.client.get("/api/usuarios/")
        assert response.status_code in {
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        }

    def test_usuario_autenticado_puede_listar_usuarios_y_roles(self):
        role, _ = RoleModel.objects.get_or_create(
            code=RolSistema.ADMINISTRADOR,
            defaults={"name": "Administrador"},
        )
        user = UsuarioModel.objects.create_user(
            username="admin",
            password="admin123",
            role=role,
        )
        self.client.force_authenticate(user=user)

        usuarios = self.client.get("/api/usuarios/")
        roles = self.client.get("/api/usuarios/roles/")

        assert usuarios.status_code == status.HTTP_200_OK
        assert roles.status_code == status.HTTP_200_OK
        assert usuarios.data[0]["username"] == "admin"

    def test_login_web_redirige_al_dashboard_del_rol_y_crea_cookies(self):
        role, _ = RoleModel.objects.get_or_create(
            code=RolSistema.LIDER_SD,
            defaults={"name": "Lider DOC"},
        )
        UsuarioModel.objects.create_user(
            username="lider",
            password="admin123",
            role=role,
        )

        response = self.client.post(
            "/login/",
            {
                "username": "lider",
                "password": "admin123",
                "recaptcha_token": "",
            },
        )

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == "/dashboard/lider-doc/"
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies

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

    def test_dashboard_redirige_por_rol_y_bloquea_dashboard_ajeno(self):
        role, _ = RoleModel.objects.get_or_create(
            code=RolSistema.ADMISIONES,
            defaults={"name": "Admisiones"},
        )
        user = UsuarioModel.objects.create_user(
            username="admisiones",
            password="admin123",
            role=role,
        )
        self.client.force_login(user)

        response = self.client.get("/dashboard/")
        forbidden_dashboard = self.client.get("/dashboard/administrador/")

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == "/dashboard/admisiones/"
        assert forbidden_dashboard.status_code == status.HTTP_302_FOUND
        assert forbidden_dashboard.url == "/dashboard/admisiones/"
