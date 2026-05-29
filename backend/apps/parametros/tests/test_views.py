from rest_framework import status
from rest_framework.test import APITestCase


class ParametrosViewsTests(APITestCase):
    def test_parametros_requiere_autenticacion(self):
        response = self.client.get("/api/parametros/")
        assert response.status_code in {
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        }
