from rest_framework import status
from rest_framework.test import APITestCase


class TestReservasView(APITestCase):
    def test_reservas_endpoint_requiere_autenticacion(self):
        response = self.client.post("/api/reservas/", {}, format="json")
        assert response.status_code in {
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        }
