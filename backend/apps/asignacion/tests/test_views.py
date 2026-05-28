from rest_framework import status
from rest_framework.test import APITestCase


class AsignacionViewsTests(APITestCase):
    def test_asignacion_requiere_autenticacion(self):
        response = self.client.get("/api/asignacion/cobertura/")
        assert response.status_code in {
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        }
