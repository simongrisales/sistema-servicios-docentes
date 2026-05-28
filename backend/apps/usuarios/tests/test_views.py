from rest_framework import status
from rest_framework.test import APITestCase


class UsuariosViewsTests(APITestCase):
    def test_perfil_requiere_autenticacion(self):
        response = self.client.get("/api/usuarios/")
        assert response.status_code in {
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        }
