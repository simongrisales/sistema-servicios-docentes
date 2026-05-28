from rest_framework import status
from rest_framework.test import APITestCase


class ReportesViewsTests(APITestCase):
    def test_reportes_requiere_autenticacion(self):
        response = self.client.get("/api/reportes/")
        assert response.status_code in {
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        }
