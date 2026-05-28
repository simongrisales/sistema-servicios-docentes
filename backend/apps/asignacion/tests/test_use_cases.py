from ..application.dtos import SimulacionInputDTO
from ..application.use_cases import AsignacionUseCaseService


def test_simular_asignacion_sin_persistir():
    output = AsignacionUseCaseService().simular_asignacion(
        SimulacionInputDTO(semestre="2026-1")
    )

    assert output.exitoso is True
