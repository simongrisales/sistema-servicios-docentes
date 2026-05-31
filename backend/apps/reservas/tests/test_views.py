from datetime import timedelta
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.academico.infrastructure.models import AulaModel
from apps.reservas.infrastructure.models import ReservaModel
from apps.usuarios.infrastructure.models import RoleModel


class TestReservasView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user_model = get_user_model()
        role, _ = RoleModel.objects.get_or_create(
            code="auxiliar_sd",
            defaults={"name": "Auxiliar SD"},
        )
        cls.user = user_model.objects.create_user(
            username="auxiliar.reservas",
            password="Test1234!",
            email="auxiliar.reservas@uco.edu.co",
            role=role,
            is_active=True,
        )
        cls.aula = AulaModel.objects.create(
            id=uuid4(),
            nombre="Aula Reserva",
            capacidad=30,
            tipo="aula_regular",
            disponible=True,
            activa=True,
        )

    def _client(self) -> APIClient:
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def test_reservas_endpoint_requiere_autenticacion(self):
        response = self.client.post("/api/reservas/", {}, format="json")
        assert response.status_code in {
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        }

    def test_reserva_pasada_devuelve_400_y_reserva_valida_aparece_en_listado(self):
        client = self._client()
        now = timezone.now()

        invalid = client.post(
            "/api/reservas/",
            {
                "aula_id": str(self.aula.id),
                "inicio": (now - timedelta(hours=2)).isoformat(),
                "fin": (now - timedelta(hours=1)).isoformat(),
                "solicitante_id": str(self.user.pk),
            },
            format="json",
        )
        assert invalid.status_code == status.HTTP_400_BAD_REQUEST
        assert "pasado" in invalid.json()["detail"]

        valid = client.post(
            "/api/reservas/",
            {
                "aula_id": str(self.aula.id),
                "inicio": (now + timedelta(hours=2)).isoformat(),
                "fin": (now + timedelta(hours=3)).isoformat(),
                "solicitante_id": str(self.user.pk),
            },
            format="json",
        )
        assert valid.status_code == status.HTTP_201_CREATED
        assert ReservaModel.objects.filter(
            reserva_id=valid.json()["reserva_id"]
        ).exists()

        listado = client.get("/api/reservas/")
        assert listado.status_code == status.HTTP_200_OK
        assert any(
            item["reserva_id"] == valid.json()["reserva_id"] for item in listado.json()
        )
