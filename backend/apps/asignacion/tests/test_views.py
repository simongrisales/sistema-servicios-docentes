"""Tests de la capa de presentacion de asignacion (API endpoints)."""

from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.asignacion.domain.exceptions import (
    AsignacionConflictoError,
    DatosIncompletosError,
)
from apps.usuarios.infrastructure.models import RoleModel, RolSistema

User = get_user_model()


def _get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class AsignacionViewsUnauthenticated(APITestCase):
    """Endpoints deben rechazar peticiones sin autenticacion."""

    def test_ejecutar_requiere_autenticacion(self):
        response = self.client.post("/api/asignacion/ejecutar/", {})
        assert response.status_code in {
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        }

    def test_simular_requiere_autenticacion(self):
        response = self.client.post("/api/asignacion/simular/", {})
        assert response.status_code in {
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        }

    def test_cobertura_requiere_autenticacion(self):
        response = self.client.get("/api/asignacion/cobertura/")
        assert response.status_code in {
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        }


class AsignacionViewsAuthenticated(APITestCase):
    """Endpoints autenticados deben responder correctamente."""

    def setUp(self):
        self.role, _ = RoleModel.objects.get_or_create(
            code=RolSistema.LIDER_SD,
            defaults={"name": "Lider DOC"},
        )
        self.user = User.objects.create_user(
            username="testdocente",
            password="Test1234!",
            role=self.role,
        )
        token = _get_tokens_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_cobertura_devuelve_200(self):
        response = self.client.get("/api/asignacion/cobertura/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_grupos" in data
        assert "grupos_con_aula" in data

    def test_simular_con_semestre_devuelve_200(self):
        payload = {"semestre": "2026-1"}
        response = self.client.post("/api/asignacion/simular/", payload, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_simular_sin_semestre_devuelve_400(self):
        response = self.client.post("/api/asignacion/simular/", {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_ejecutar_datos_invalidos_devuelve_400(self):
        """Payload vacio debe fallar la validacion del serializador."""
        response = self.client.post("/api/asignacion/ejecutar/", {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_ejecutar_conflicto_devuelve_409(self):
        servicio = MagicMock()
        servicio.ejecutar_asignacion_automatica.side_effect = AsignacionConflictoError(
            ["El aula ya esta ocupada en ese bloque."]
        )

        with patch(
            "apps.asignacion.presentation.views.AsignacionViewSet._service",
            return_value=servicio,
        ):
            response = self.client.post(
                "/api/asignacion/ejecutar/",
                {
                    "grupo_id": "1",
                    "aula_id": "1",
                    "bloque_horario_id": "1",
                    "semestre": "2026-1",
                },
                format="json",
            )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert "aula ya esta ocupada" in response.data["detail"].lower()

    def test_ejecutar_semestre_datos_incompletos_devuelve_400(self):
        servicio = MagicMock()
        servicio.ejecutar_asignacion_automatica_semestre.side_effect = (
            DatosIncompletosError("No hay aulas disponibles para el semestre 2026-1.")
        )

        with patch(
            "apps.asignacion.presentation.views.AsignacionViewSet._service",
            return_value=servicio,
        ):
            response = self.client.post(
                "/api/asignacion/ejecutar-semestre/",
                {"semestre": "2026-1"},
                format="json",
            )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "No hay aulas disponibles" in response.data["detail"]
