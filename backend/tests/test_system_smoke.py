from datetime import time

from django.contrib.auth import authenticate, get_user_model
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.academico.infrastructure.models import (
    AulaModel,
    CursoModel,
    DocenteModel,
    FacultadModel,
    GrupoModel,
    HorarioBloqueModel,
    ProgramaModel,
)
from apps.asignacion.infrastructure.models import AsignacionModel
from apps.parametros.infrastructure.models import CatalogoParametroModel
from apps.usuarios.infrastructure.models import RoleModel
from apps.usuarios.management.commands.seed_base_data import DEMO_PASSWORD


class SistemaSmokeTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        call_command("seed_base_data")
        cls.user_model = get_user_model()
        cls._ensure_smoke_data()
        cls.admin = cls.user_model.objects.get(username="admin.sds")
        cls.access_token = str(RefreshToken.for_user(cls.admin).access_token)

    @classmethod
    def _ensure_smoke_data(cls) -> None:
        if AulaModel.objects.exists():
            return

        role, _ = RoleModel.objects.get_or_create(
            code="facultad",
            defaults={"name": "Facultad"},
        )
        usuario, _ = cls.user_model.objects.get_or_create(
            username="docente.smoke",
            defaults={
                "email": "docente.smoke@uco.edu.co",
                "role": role,
                "departamento": "Facultad Ingenieria",
                "cargo": "Docente",
                "is_active": True,
            },
        )
        usuario.set_password(DEMO_PASSWORD)
        usuario.save(update_fields=["password"])

        facultad, _ = FacultadModel.objects.get_or_create(
            codigo="SMK",
            defaults={"nombre": "Facultad Smoke", "activa": True},
        )
        programa, _ = ProgramaModel.objects.get_or_create(
            codigo="SMK-GEN",
            defaults={
                "facultad": facultad,
                "nombre": "Programa Smoke",
                "activo": True,
            },
        )
        docente, _ = DocenteModel.objects.get_or_create(
            email="smoke.docente@uco.edu.co",
            defaults={
                "nombre": "Docente Smoke",
                "activo": True,
                "usuario": usuario,
            },
        )
        curso, _ = CursoModel.objects.get_or_create(
            codigo="SMK101",
            defaults={
                "programa": programa,
                "nombre": "Curso Smoke",
                "creditos": 3,
                "activo": True,
            },
        )
        AulaModel.objects.get_or_create(
            nombre="Aula Smoke 101",
            defaults={
                "capacidad": 40,
                "tipo": "aula_regular",
                "disponible": True,
                "restricciones": {},
                "activa": True,
            },
        )
        HorarioBloqueModel.objects.get_or_create(
            dia="lunes",
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            defaults={"activo": True},
        )
        GrupoModel.objects.get_or_create(
            curso=curso,
            codigo="SMK-01",
            semestre="2026-1",
            defaults={
                "docente": docente,
                "num_estudiantes": 24,
                "activo": True,
            },
        )
        CatalogoParametroModel.objects.get_or_create(
            clave="max_aulas_por_semestre",
            defaults={
                "valor": 10,
                "grupo": "asignacion",
                "descripcion": "Parametro base de smoke test",
                "activo": True,
            },
        )

    def _api_client(self) -> APIClient:
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        return client

    def test_login_demo_y_token_api_funcionan(self) -> None:
        web_client = Client()
        response = web_client.post(
            reverse("login"),
            {
                "username": "admin.sds",
                "password": DEMO_PASSWORD,
                "recaptcha_token": "",
            },
        )

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == reverse("dashboard_administrador")

        token_response = web_client.post(
            reverse("token_obtain_pair"),
            {"username": "admin.sds", "password": DEMO_PASSWORD},
        )

        assert token_response.status_code == status.HTTP_200_OK
        assert "access" in token_response.json()
        assert "refresh" in token_response.json()
        assert authenticate(username="admin.sds", password=DEMO_PASSWORD) is not None

    def test_catalogos_academicos_y_parametros_se_consultan(self) -> None:
        client = self._api_client()

        aulas = client.get("/api/academico/aulas/")
        bloques = client.get("/api/academico/aulas/bloques/")
        cursos = client.get("/api/academico/aulas/cursos/")
        docentes = client.get("/api/academico/aulas/docentes/")
        grupos = client.get("/api/academico/aulas/grupos/")
        parametros = client.get("/api/parametros/")
        roles = client.get("/api/usuarios/roles/")

        assert aulas.status_code == status.HTTP_200_OK
        assert bloques.status_code == status.HTTP_200_OK
        assert cursos.status_code == status.HTTP_200_OK
        assert docentes.status_code == status.HTTP_200_OK
        assert grupos.status_code == status.HTTP_200_OK
        assert parametros.status_code == status.HTTP_200_OK
        assert roles.status_code == status.HTTP_200_OK
        assert len(aulas.json()) > 0
        assert len(bloques.json()) > 0
        assert len(cursos.json()) > 0
        assert len(docentes.json()) > 0
        assert len(grupos.json()) > 0
        assert any(
            item["clave"] == "max_aulas_por_semestre" for item in parametros.json()
        )
        assert any(item["code"] == "administrador" for item in roles.json())

    def test_creacion_de_usuario_aula_parametro_y_grupo(self) -> None:
        client = self._api_client()

        nuevo_usuario = client.post(
            "/api/usuarios/crear/",
            {
                "username": "nuevo.demo",
                "email": "nuevo.demo@uco.edu.co",
                "password": "Demo1234!",
                "role_code": "facultad",
                "departamento": "Facultad Ingenieria",
                "cargo": "Analista",
            },
            format="json",
        )
        assert nuevo_usuario.status_code == status.HTTP_201_CREATED
        assert self.user_model.objects.filter(username="nuevo.demo").exists()
        assert authenticate(username="nuevo.demo", password="Demo1234!") is not None

        nueva_aula = client.post(
            "/api/academico/aulas/",
            {
                "nombre": "Aula Presentacion 401",
                "capacidad": 40,
                "tipo": "aula_regular",
                "disponible": True,
            },
            format="json",
        )
        assert nueva_aula.status_code == status.HTTP_201_CREATED
        assert AulaModel.objects.filter(nombre="Aula Presentacion 401").exists()

        nuevo_parametro = client.post(
            "/api/parametros/",
            {
                "clave": "modo_presentacion",
                "valor": True,
                "grupo": "general",
                "descripcion": "Parametro demo para sustentacion",
                "activo": True,
            },
            format="json",
        )
        assert nuevo_parametro.status_code == status.HTTP_201_CREATED
        assert CatalogoParametroModel.objects.filter(clave="modo_presentacion").exists()

        curso = CursoModel.objects.filter(activo=True).order_by("codigo").first()
        docente = DocenteModel.objects.filter(activo=True).order_by("nombre").first()
        assert curso is not None
        assert docente is not None

        nuevo_grupo = client.post(
            "/api/academico/aulas/grupos/",
            {
                "curso_id": str(curso.id),
                "docente_id": str(docente.id),
                "codigo": "SMOKE-01",
                "num_estudiantes": 24,
                "semestre": "2026-1",
            },
            format="json",
        )
        assert nuevo_grupo.status_code == status.HTTP_201_CREATED
        assert GrupoModel.objects.filter(codigo="SMOKE-01").exists()

    def test_asignacion_automatica_y_cobertura_reporta_resultado(self) -> None:
        client = self._api_client()

        grupo = self._select_grupo_con_capacidad()
        aula = (
            AulaModel.objects.filter(
                activa=True,
                disponible=True,
                capacidad__gte=grupo.num_estudiantes,
            )
            .order_by("capacidad", "nombre")
            .first()
        )
        bloque = self._select_bloque_disponible()

        assert aula is not None
        assert bloque is not None

        resultado = client.post(
            "/api/asignacion/ejecutar/",
            {
                "grupo_id": str(grupo.id),
                "aula_id": str(aula.id),
                "bloque_horario_id": str(bloque.id),
                "semestre": grupo.semestre,
            },
            format="json",
        )
        assert resultado.status_code == status.HTTP_201_CREATED
        assert AsignacionModel.objects.filter(
            grupo_id=grupo.id,
            aula_id=aula.id,
            bloque_horario_id=bloque.id,
            semestre=grupo.semestre,
            estado="CONFIRMADO",
        ).exists()

        cobertura = client.get(
            "/api/asignacion/cobertura/",
            {"semestre": grupo.semestre},
        )
        assert cobertura.status_code == status.HTTP_200_OK
        assert cobertura.json()["total_grupos"] > 0
        assert cobertura.json()["grupos_con_aula"] >= 1

        simulacion = client.post(
            "/api/asignacion/simular/",
            {
                "semestre": grupo.semestre,
                "grupos": [
                    {"id": str(grupo.id), "num_estudiantes": grupo.num_estudiantes}
                ],
                "aulas": [
                    {
                        "id": str(aula.id),
                        "capacidad": aula.capacidad,
                        "disponible": True,
                    }
                ],
            },
            format="json",
        )
        assert simulacion.status_code == status.HTTP_200_OK
        assert "exitoso" in simulacion.json()

    @staticmethod
    def _select_grupo_con_capacidad():
        grupo = (
            GrupoModel.objects.filter(activo=True)
            .order_by("num_estudiantes", "codigo")
            .first()
        )
        assert grupo is not None
        return grupo

    @staticmethod
    def _select_bloque_disponible():
        bloque = (
            HorarioBloqueModel.objects.filter(activo=True)
            .order_by("dia", "hora_inicio")
            .first()
        )
        assert bloque is not None
        return bloque
