# reportes/application/dtos.py
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class ReporteInputDTO:
    """Data Transfer Object para solicitar la generación de un reporte."""
    reporte_tipo_codigo: str # Código del tipo de reporte (ej: OCCU, COV)
    periodo_inicio: date
    periodo_fin: date
    usuario_id: int

@dataclass
class ReporteOutputDTO:
    """Datos estructurados que contienen el resultado final del reporte."""
    reporte_id: int # ID único en la BD
    titulo: str
    estado: str = "COMPLETO"
    contenido_estructurado: Optional[dict] = None # Datos finales, listos para mostrar/descargar.

@dataclass
class SimulaciónInputDTO:
    """Datos de entrada para simular escenarios sin afectar datos reales."""
    periodo_inicio: date
    periodo_fin: date
    parametros_extra: dict = field(default_factory=dict)