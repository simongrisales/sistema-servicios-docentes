from django.contrib.auth import authenticate, get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.usuarios.infrastructure.models import RoleModel
from apps.usuarios.management.commands.seed_base_data import (
    DEMO_PASSWORD,
    DEMO_USERS,
)


class SeedBaseDataTests(TestCase):
    def test_seed_base_data_crea_usuarios_demo_y_roles(self) -> None:
        call_command("seed_base_data")

        user_model = get_user_model()
        expected_users = {username for username, *_ in DEMO_USERS}

        assert RoleModel.objects.filter(
            code__in=[item[2] for item in DEMO_USERS]
        ).count() == len(DEMO_USERS)
        assert user_model.objects.filter(username__in=expected_users).count() == len(
            DEMO_USERS
        )

        for username, email, role_code, departamento in DEMO_USERS:
            user = user_model.objects.get(username=username)
            assert user.email == email
            assert user.role.code == role_code
            assert user.departamento == departamento
            assert authenticate(username=username, password=DEMO_PASSWORD) is not None

    def test_login_demo_funciona_con_las_credenciales_base(self) -> None:
        call_command("seed_base_data")

        response = self.client.post(
            reverse("login"),
            {
                "username": "admin.sds",
                "password": DEMO_PASSWORD,
                "recaptcha_token": "",
            },
        )

        assert response.status_code == 302
        assert response.url == reverse("dashboard_administrador")
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies
