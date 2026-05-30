"""Tests de la capa de aplicacion de asignacion (use cases)."""

from unittest.mock import MagicMock

import pytest

from ..application.dtos import (
    AsignacionInputDTO,
    AsignacionOutputDTO,
    SimulacionInputDTO,
)
from ..application.use_cases import AsignacionUseCaseService
from ..domain.entities import Asignacion, ResultadoAsignacion
from ..domain.exceptions import (
    AsignacionConflictoError,
    CapacidadInsuficienteError,
    DatosIncompletosError,
)
from ..infrastructure.tasks import (
    asignacion_automatica_task,
    asignacion_masiva_task,
    recalculo_automatico_task,
    recalculo_task,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_service(
    existe_conflicto: bool = False,
    strategy_exitosa: bool = True,
) -> AsignacionUseCaseService:
    """Construye el servicio con mocks controlados."""
    repo_mock = MagicMock()
    repo_mock.existe_conflicto.return_value = existe_conflicto
    repo_mock.guardar.side_effect = lambda asignacion: Asignacion(
        id=1,
        grupo_id=asignacion.grupo_id,
        aula_id=asignacion.aula_id,
        bloque_horario_id=asignacion.bloque_horario_id,
        semestre=asignacion.semestre,
        estado=asignacion.estado,
    )
    # _validar_capacidad accede a obtener_grupo/obtener_aula: devolvemos None
    # para que el método salga sin comparar MagicMock entre sí.
    repo_mock.obtener_grupo.return_value = None
    repo_mock.obtener_aula.return_value = None

    strategy_mock = MagicMock()
    strategy_mock.asignar.return_value = ResultadoAsignacion(
        exitoso=strategy_exitosa,
        mensaje="OK" if strategy_exitosa else "Fallo",
        conflicto_detalles=[] if strategy_exitosa else ["Conflicto X"],
        asignaciones=[
            {
                "grupo_id": "1",
                "aula_id": "2",
                "bloque_horario_id": "3",
                "semestre": "2026-1",
                "estado": "CONFIRMADO",
            }
        ],
    )
    notificacion_mock = MagicMock()

    return AsignacionUseCaseService(
        asignacion_repo=repo_mock,
        strategy=strategy_mock,
        notificacion_service=notificacion_mock,
    )


class _RepoSinMetodosCapacidad:
    def existe_conflicto(self, *args, **kwargs):
        return False

    def guardar(self, asignacion):
        return asignacion


class _Grupo:
    num_estudiantes = 20


class _Aula:
    capacidad = 10


def _input_dto() -> AsignacionInputDTO:
    return AsignacionInputDTO(
        grupo_id="10",
        aula_id="20",
        bloque_horario_id="30",
        semestre="2026-1",
    )


# ---------------------------------------------------------------------------
# ejecutar_asignacion_automatica
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestEjecutarAsignacionAutomatica:
    def test_asignacion_exitosa_devuelve_output_dto(self):
        service = _make_service(existe_conflicto=False)
        output = service.ejecutar_asignacion_automatica(_input_dto())

        assert isinstance(output, AsignacionOutputDTO)
        assert output.grupo_id == "10"
        assert output.aula_id == "20"
        assert output.semestre == "2026-1"
        assert output.estado == "CONFIRMADO"

    def test_asignacion_con_conflicto_lanza_excepcion(self):
        service = _make_service(existe_conflicto=True)

        with pytest.raises(AsignacionConflictoError) as exc_info:
            service.ejecutar_asignacion_automatica(_input_dto())

        assert "El aula ya esta ocupada" in str(exc_info.value.detalles_conflicto)

    def test_asignacion_sin_repositorio_no_persiste(self):
        """Cuando no se inyecta repo, la asignacion se crea sin persistir."""
        service = AsignacionUseCaseService()
        output = service.ejecutar_asignacion_automatica(_input_dto())

        # id=0 indica que no se persistio
        assert output.grupo_id == "10"
        assert output.estado == "CONFIRMADO"

    def test_repo_guardar_es_llamado(self):
        service = _make_service(existe_conflicto=False)
        service.ejecutar_asignacion_automatica(_input_dto())

        service.asignacion_repo.guardar.assert_called_once()

    def test_validar_conflictos_horario_lanza_excepcion(self):
        service = _make_service(existe_conflicto=True)

        with pytest.raises(AsignacionConflictoError):
            service.validar_conflictos_horario("20", "30", "10", "2026-1")

    def test_asignacion_masiva_sin_grupos_lanza_excepcion(self):
        service = _make_service()

        with pytest.raises(DatosIncompletosError):
            service.ejecutar_asignacion_automatica_semestre(
                "2026-1",
                grupos=[],
                aulas=[{"id": "a1", "capacidad": 20, "disponible": True, "activa": True}],
            )

    def test_asignacion_masiva_llama_repo_y_notificacion(self):
        from django.contrib.auth import get_user_model

        get_user_model().objects.get_or_create(
            username="admin.tests",
            defaults={
                "is_staff": True,
                "is_superuser": True,
                "email": "admin.tests@uco.edu.co",
            },
        )

        service = _make_service()
        resultado = service.ejecutar_asignacion_automatica_semestre(
            "2026-1",
            grupos=[
                {
                    "id": "g1",
                    "num_estudiantes": 10,
                    "bloque_horario_id": "b1",
                    "semestre": "2026-1",
                }
            ],
            aulas=[
                {"id": "a1", "capacidad": 20, "disponible": True, "activa": True},
            ],
        )

        assert resultado.estado == "RESUMEN"
        assert resultado.total_asignaciones == 1
        service.asignacion_repo.guardar.assert_called()
        service.notificacion_service.enviar_notificacion.assert_called_once()


# ---------------------------------------------------------------------------
# simular_asignacion
# ---------------------------------------------------------------------------


class TestSimularAsignacion:
    def test_simulacion_sin_strategy_es_exitosa(self):
        service = AsignacionUseCaseService()
        output = service.simular_asignacion(SimulacionInputDTO(semestre="2026-1"))

        assert output.exitoso is True
        assert "sin persistir" in output.mensaje.lower()

    def test_simulacion_con_strategy_exitosa(self):
        service = _make_service(strategy_exitosa=True)
        output = service.simular_asignacion(
            SimulacionInputDTO(semestre="2026-1", grupos=[{"id": 1}], aulas=[{"id": 2}])
        )

        assert output.exitoso is True
        assert output.mensaje == "OK"

    def test_simulacion_con_strategy_fallida(self):
        service = _make_service(strategy_exitosa=False)
        output = service.simular_asignacion(SimulacionInputDTO(semestre="2026-1"))

        assert output.exitoso is False
        assert "Conflicto X" in output.conflictos


# ---------------------------------------------------------------------------
# verificar_cobertura_total
# ---------------------------------------------------------------------------


class TestVerificarCoberturaTotal:
    def test_cobertura_devuelve_dto(self):
        service = AsignacionUseCaseService()
        output = service.verificar_cobertura_total()

        assert output.total_grupos == 0
        assert output.grupos_con_aula == 0

    def test_cobertura_con_repositorio_devuelve_totales(self):
        repo_mock = MagicMock()
        repo_mock.contar_grupos_por_semestre.return_value = 12
        repo_mock.contar_grupos_asignados_por_semestre.return_value = 9

        service = AsignacionUseCaseService(asignacion_repo=repo_mock)
        output = service.verificar_cobertura_total("2026-1")

        assert output.total_grupos == 12
        assert output.grupos_con_aula == 9


class TestValidarCapacidad:
    def test_validar_capacidad_sin_metodos_no_falla(self):
        service = AsignacionUseCaseService(asignacion_repo=_RepoSinMetodosCapacidad())

        output = service.ejecutar_asignacion_automatica(_input_dto())

        assert output.estado == "CONFIRMADO"

    def test_validar_capacidad_lanza_excepcion_si_aula_no_alcanza(self):
        repo_mock = MagicMock()
        repo_mock.existe_conflicto.return_value = False
        repo_mock.obtener_grupo.return_value = _Grupo()
        repo_mock.obtener_aula.return_value = _Aula()

        service = AsignacionUseCaseService(asignacion_repo=repo_mock)

        with pytest.raises(CapacidadInsuficienteError):
            service.ejecutar_asignacion_automatica(_input_dto())


class TestTareasCeleryAsignacion:
    pytestmark = pytest.mark.django_db

    def test_asignacion_automatica_task_devuelve_resumen(self):
        resultado = asignacion_automatica_task.run("2026-1")

        assert resultado["semestre_id"] == "2026-1"
        assert resultado["estado"] in {"completada", "fallida"}
        assert "detalle" in resultado or "total_asignaciones" in resultado

    def test_recalculo_task_devuelve_estado(self):
        resultado = recalculo_task.run("2026-1")

        assert resultado["semestre_id"] == "2026-1"
        assert resultado["estado"] == "programado"

    def test_asignacion_masiva_task_cuenta_grupos(self):
        resultado = asignacion_masiva_task.run([1, 2, 3], "2026-1")

        assert resultado["total_procesados"] == 3
        assert resultado["semestre"] == "2026-1"

    def test_recalculo_automatico_task_legacy(self):
        resultado = recalculo_automatico_task.run()

        assert resultado["estado"] == "programado"

    def test_recalculo_automatico_task_con_contexto(self):
        resultado = recalculo_automatico_task.run("grupo-1", "2026-1")

        assert resultado["grupo_id"] == "grupo-1"
        assert resultado["semestre_id"] == "2026-1"
