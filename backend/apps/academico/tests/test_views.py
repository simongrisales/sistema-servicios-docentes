from rest_framework import status
from rest_framework.test import APITestCase


class AcademicoViewsTests(APITestCase):
    def test_academico_requiere_autenticacion(self):
        response = self.client.get("/api/academico/aulas/")
        assert response.status_code in {
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        }
