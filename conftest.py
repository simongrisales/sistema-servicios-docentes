"""
conftest.py — Configuración raíz de pytest para el Sistema de Servicios Docentes.

Proporciona:
- Configuración de Django para pytest-django
- Fixtures compartidas reutilizables entre todas las apps
"""

import django
import pytest


# ---------------------------------------------------------------------------
# Fixtures compartidas
# ---------------------------------------------------------------------------


@pytest.fixture
def api_client():
    """Cliente REST sin autenticación."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def usuario_test(db):
    """Crea y retorna un usuario de prueba sin roles especiales."""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    return User.objects.create_user(
        username="test_user",
        email="test@uco.edu.co",
        password="Test1234!",
    )


@pytest.fixture
def api_client_autenticado(api_client, usuario_test):
    """Cliente REST autenticado con JWT Bearer token."""
    from rest_framework_simplejwt.tokens import RefreshToken

    token = str(RefreshToken.for_user(usuario_test).access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client
