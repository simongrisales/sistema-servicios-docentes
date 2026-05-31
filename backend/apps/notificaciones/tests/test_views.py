from uuid import uuid4

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.notificaciones.infrastructure.models import NotificacionModel
from apps.usuarios.infrastructure.models import RoleModel


class NotificacionesViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user_model = get_user_model()
        role, _ = RoleModel.objects.get_or_create(
            code="auxiliar_sd",
            defaults={"name": "Auxiliar SD"},
        )
        cls.user = user_model.objects.create_user(
            username="notif.user",
            password="Test1234!",
            email="notif.user@uco.edu.co",
            role=role,
            is_active=True,
        )
        cls.notification = NotificacionModel.objects.create(
            notificacion_id=str(uuid4()),
            tipo="conflicto_detectado",
            titulo="Conflicto detectado",
            mensaje="Aula ocupada",
            usuario_destino=cls.user,
            lectura_requerida=True,
            es_leida=False,
            activo=True,
        )

    def _client(self) -> APIClient:
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def test_eliminar_notificacion_desactiva_y_devuelve_204(self):
        response = self._client().delete(
            f"/api/notificaciones/{self.notification.notificacion_id}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        self.notification.refresh_from_db()
        assert self.notification.activo is False
