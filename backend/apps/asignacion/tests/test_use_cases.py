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
from ..domain.exceptions import AsignacionConflictoError

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

    strategy_mock = MagicMock()
    strategy_mock.asignar.return_value = ResultadoAsignacion(
        exitoso=strategy_exitosa,
        mensaje="OK" if strategy_exitosa else "Fallo",
        conflicto_detalles=[] if strategy_exitosa else ["Conflicto X"],
    )

    return AsignacionUseCaseService(asignacion_repo=repo_mock, strategy=strategy_mock)


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
