from datetime import date

from ..domain.entities import Reporte


def test_reporte_entidad_conserva_estado():
    reporte = Reporte(
        tipo_codigo="OCUPACION",
        titulo="Ocupacion",
        fecha_generacion=date.today(),
        periodo_inicio=date.today(),
        periodo_fin=date.today(),
        descripcion_detallada="",
        usuario_solicitante_id=1,
    )

    assert reporte.estado == "PENDIENTE"
