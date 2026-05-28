from datetime import date

from ..application.dtos import SimulacionInputDTO
from ..application.use_cases import ReporteService


def test_simular_reporte_devuelve_estado_simulado():
    output = ReporteService().simular_generacion(
        SimulacionInputDTO(
            periodo_inicio=date.today(),
            periodo_fin=date.today(),
        )
    )

    assert output.estado == "SIMULADO"
