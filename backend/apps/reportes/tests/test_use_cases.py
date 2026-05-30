from datetime import date

import pytest

from ..application.dtos import ReporteInputDTO, SimulacionInputDTO
from ..application.use_cases import ReporteService
from ..domain.entities import Reporte
from ..domain.exceptions import TipoReporteInvalidoError


def test_simular_reporte_devuelve_estado_simulado():
    output = ReporteService().simular_generacion(
        SimulacionInputDTO(
            periodo_inicio=date.today(),
            periodo_fin=date.today(),
        )
    )

    assert output.estado == "SIMULADO"


class FakeReporteRepository:
    def __init__(self, reporte: Reporte | None = None) -> None:
        self.reporte = reporte
        self.created_request = None

    def create_report_request(self, reporte: Reporte) -> int:
        self.created_request = reporte
        return 42

    def get_reporte_by_id(self, reporte_id: int):
        if self.reporte and self.reporte.reporte_id == reporte_id:
            return self.reporte
        return None


def test_ejecutar_generacion_sin_repo_retorna_cero():
    output = ReporteService().ejecutar_generacion_asincrona(
        ReporteInputDTO(
            reporte_tipo_codigo="OCUPACION",
            periodo_inicio=date(2026, 1, 1),
            periodo_fin=date(2026, 6, 30),
            usuario_id=1,
        )
    )

    assert output == 0


def test_ejecutar_generacion_con_repo_crea_solicitud():
    repo = FakeReporteRepository()

    output = ReporteService(repo).ejecutar_generacion_asincrona(
        ReporteInputDTO(
            reporte_tipo_codigo="COBERTURA",
            periodo_inicio=date(2026, 1, 1),
            periodo_fin=date(2026, 6, 30),
            usuario_id=7,
        )
    )

    assert output == 42
    assert repo.created_request.usuario_solicitante_id == 7
    assert repo.created_request.estado == "PENDIENTE"


def test_ejecutar_generacion_rechaza_tipo_invalido():
    with pytest.raises(TipoReporteInvalidoError):
        ReporteService().ejecutar_generacion_asincrona(
            ReporteInputDTO(
                reporte_tipo_codigo="DESCONOCIDO",
                periodo_inicio=date(2026, 1, 1),
                periodo_fin=date(2026, 6, 30),
                usuario_id=1,
            )
        )


def test_obtener_estado_reporte_sin_repo_devuelve_pendiente():
    output = ReporteService().obtener_estado_reporte(99)

    assert output.reporte_id == 99
    assert output.estado == "PENDIENTE"


def test_obtener_estado_reporte_existente_e_inexistente():
    reporte = Reporte(
        reporte_id=3,
        tipo_codigo="ASIGNACIONES",
        titulo="Asignaciones",
        fecha_generacion=date.today(),
        periodo_inicio=date(2026, 1, 1),
        periodo_fin=date(2026, 6, 30),
        descripcion_detallada="Detalle",
        estado="COMPLETO",
        usuario_solicitante_id=1,
        datos_raw={"total": 10},
    )
    service = ReporteService(FakeReporteRepository(reporte))

    output = service.obtener_estado_reporte(3)

    assert output.contenido_estructurado == {"total": 10}
    with pytest.raises(ValueError, match="Reporte no encontrado"):
        service.obtener_estado_reporte(4)
