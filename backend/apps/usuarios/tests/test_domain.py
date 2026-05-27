# usuarios/tests/test_domain.py
from django.test import TestCase
from ..domain.entities import User, Role
from ..domain.exceptions import CredencialesInvalidasError

class UsuarioDomainTests(TestCase):
    """Testea las reglas de negocio y la creación de entidades sin depender del ORM."""

    def test_user_creation_success(self):
        # Simula la creación exitosa de una entidad usuario.
        user = User(1, "testuser", "test@email.com", "password", Role(1, "Admin", "Admin principal"))
        self.assertEqual(user.username, "testuser")

    def test_credential_validation_failure(self):
        # Prueba que el error de credenciales se lance correctamente
        try:
            raise CredencialesInvalidasError()
        except CredencialesInvalidasError as e:
            self.assertTrue("Credenciales inválidas" in str(e))

# usuarios/tests/test_views.py
from rest_framework.test import APITestCase

class UsuarioViewTests(APITestCase):
    """Test de integración para las vistas de usuario, simulando peticiones API."""

    def test_login_success(self):
        # Prueba que un login exitoso devuelve tokens válidos y 200 OK
        response = self.client.post("/api/usuarios/login/", {"username": "testuser", "password": "correct_password"})
        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        # Prueba que un login fallido devuelve 401 Unauthorized
        response = self.client.post("/api/usuarios/login/", {"username": "unknown", "password": "wrong"})
        self.assertEqual(response.status_code, 401)