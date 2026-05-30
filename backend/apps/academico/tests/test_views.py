from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.academico.infrastructure.models import AulaModel, FacultadModel, ProgramaModel
from apps.usuarios.infrastructure.models import RoleModel


class AcademicoViewsTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_model = get_user_model()
        role, _ = RoleModel.objects.get_or_create(
            code="administrador",
            defaults={"name": "Administrador"},
        )
        cls.admin_user, _ = cls.user_model.objects.get_or_create(
            username="adminsd.test",
            defaults={
                "email": "adminsd.test@uco.edu.co",
                "role": role,
                "departamento": "TI",
                "cargo": "Administrador",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )
        facultad, _ = FacultadModel.objects.get_or_create(
            codigo="ING",
            defaults={"nombre": "Facultad de Ingeniería", "activa": True},
        )
        ProgramaModel.objects.get_or_create(
            codigo="ING-GEN",
            defaults={
                "facultad": facultad,
                "nombre": "Ingeniería de Sistemas",
                "activo": True,
            },
        )
        AulaModel.objects.get_or_create(
            nombre="Aula Test 101",
            defaults={
                "capacidad": 40,
                "tipo": "aula_regular",
                "disponible": True,
                "restricciones": {},
                "activa": True,
            },
        )
        cls.admin = cls.admin_user

    def _client(self) -> APIClient:
        client = APIClient()
        client.force_authenticate(user=self.admin)
        return client

    def test_academico_requiere_autenticacion(self):
        response = self.client.get("/api/academico/aulas/")
        assert response.status_code in {
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        }

    def test_catalogos_de_facultades_programas_busqueda_y_estado_aula(self):
        client = self._client()

        facultades = client.get("/api/academico/aulas/facultades/")
        assert facultades.status_code == status.HTTP_200_OK
        assert len(facultades.json()) > 0
        assert any(item["programas"] >= 1 for item in facultades.json())

        facultad = FacultadModel.objects.filter(activa=True).order_by("nombre").first()
        assert facultad is not None

        programas = client.get(
            "/api/academico/aulas/programas/",
            {"facultad_id": str(facultad.id)},
        )
        assert programas.status_code == status.HTTP_200_OK
        assert len(programas.json()) > 0
        assert all(
            str(item["facultad_id"]) == str(facultad.id) for item in programas.json()
        )

        aula = AulaModel.objects.filter(activa=True).order_by("nombre").first()
        assert aula is not None

        busqueda = client.get(
            "/api/academico/aulas/buscar/",
            {"q": aula.nombre.split()[0]},
        )
        assert busqueda.status_code == status.HTTP_200_OK
        assert any(str(item["id"]) == str(aula.id) for item in busqueda.json())

        estado_original = aula.disponible
        nuevo_estado = client.patch(
            f"/api/academico/aulas/{aula.id}/estado/",
            {"disponible": not aula.disponible},
            format="json",
        )
        assert nuevo_estado.status_code == status.HTTP_200_OK
        aula.refresh_from_db()
        assert aula.disponible == nuevo_estado.json()["disponible"]
        assert aula.disponible is not estado_original
