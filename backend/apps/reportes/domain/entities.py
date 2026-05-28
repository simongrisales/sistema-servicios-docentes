from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class ReporteTipo:
    codigo: str
    nombre_completo: str
    descripcion: str


@dataclass(frozen=True)
class Reporte:
    tipo_codigo: str
    titulo: str
    fecha_generacion: date
    periodo_inicio: date
    periodo_fin: date
    descripcion_detallada: str
    usuario_solicitante_id: int
    reporte_id: int | None = None
    estado: str = "PENDIENTE"
    datos_raw: dict[str, Any] | None = None


@dataclass(frozen=True)
class DatoReporteItem:
    key: str
    valor: Any
    detalle: str | None = None
