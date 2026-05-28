from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class ReporteInputDTO:
    reporte_tipo_codigo: str
    periodo_inicio: date
    periodo_fin: date
    usuario_id: int


@dataclass(frozen=True)
class ReporteOutputDTO:
    reporte_id: int
    titulo: str
    estado: str = "COMPLETO"
    contenido_estructurado: dict | None = None


@dataclass(frozen=True)
class SimulacionInputDTO:
    periodo_inicio: date
    periodo_fin: date
    parametros_extra: dict = field(default_factory=dict)
