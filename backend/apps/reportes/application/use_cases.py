from datetime import date

from ..domain.entities import Reporte
from ..domain.exceptions import TipoReporteInvalidoError
from ..domain.interfaces import IReporteRepository
from .dtos import ReporteInputDTO, ReporteOutputDTO, SimulacionInputDTO


class ReporteService:
    """Casos de uso para solicitudes, consulta y simulacion de reportes."""

    TIPOS_VALIDOS = {"OCUPACION", "COBERTURA", "ASIGNACIONES"}

    def __init__(self, reporte_repo: IReporteRepository | None = None) -> None:
        self.reporte_repo = reporte_repo

    def ejecutar_generacion_asincrona(self, dto: ReporteInputDTO) -> int:
        self._validar_reporte_tipo(dto.reporte_tipo_codigo)
        reporte = Reporte(
            tipo_codigo=dto.reporte_tipo_codigo,
            titulo=f"Reporte {dto.reporte_tipo_codigo}",
            fecha_generacion=date.today(),
            periodo_inicio=dto.periodo_inicio,
            periodo_fin=dto.periodo_fin,
            descripcion_detallada="Solicitud de generacion asincrona.",
            estado="PENDIENTE",
            usuario_solicitante_id=dto.usuario_id,
        )
        if self.reporte_repo is None:
            return 0
        return self.reporte_repo.create_report_request(reporte)

    def obtener_estado_reporte(self, reporte_id: int) -> ReporteOutputDTO:
        if self.reporte_repo is None:
            return ReporteOutputDTO(
                reporte_id=reporte_id,
                titulo="Reporte no consultado",
                estado="PENDIENTE",
            )
        reporte = self.reporte_repo.get_reporte_by_id(reporte_id)
        if reporte is None:
            raise ValueError("Reporte no encontrado.")
        return ReporteOutputDTO(
            reporte_id=reporte.reporte_id or reporte_id,
            titulo=reporte.titulo,
            estado=reporte.estado,
            contenido_estructurado=reporte.datos_raw,
        )

    def simular_generacion(self, dto: SimulacionInputDTO) -> ReporteOutputDTO:
        return ReporteOutputDTO(
            reporte_id=0,
            titulo=f"Simulacion {dto.periodo_inicio} - {dto.periodo_fin}",
            estado="SIMULADO",
            contenido_estructurado={"parametros": dto.parametros_extra},
        )

    def _validar_reporte_tipo(self, codigo: str) -> None:
        if codigo not in self.TIPOS_VALIDOS:
            raise TipoReporteInvalidoError(f"Tipo de reporte no valido: {codigo}")
