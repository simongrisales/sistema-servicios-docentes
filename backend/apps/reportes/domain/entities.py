# reportes/domain/entities.py
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

@dataclass
class ReporteTipo:
    """Representa el tipo de reporte (Ej: Ocupación, Cobertura)."""
    codigo: str # Código único del tipo de reporte (ej: OCCU)
    nombre_completo: str
    descripcion: str
    icon_name: str = "fa-file-alt"

@dataclass
class Reporte:
    """Representa un reporte generado."""
    reporte_id: Optional[int] = None
    tipo_codigo: str # Código del ReporteTipo que lo generó
    titulo: str
    fecha_generacion: date
    periodo_inicio: date
    periodo_fin: date
    descripcion_detallada: str
    estado: str = "PENDIENTE"  # PENDIENTE, GENERANDO, COMPLETO, FALLIDO
    usuario_solicitante_id: int # ID del usuario que lo solicitó
    datos_raw: Optional[dict] = None # Datos brutos (JSONB) almacenados en la DB

@dataclass
class DatoReporteItem:
    """Representa un elemento de dato dentro de un reporte."""
    key: str
    valor: any
    detalle: Optional[str] = None