# reportes/domain/interfaces.py
from abc import ABC, abstractmethod
from typing import List, Dict

class IReporteRepository(ABC):
    """Interfaz de Repositorio para la gestión del ciclo de vida de los Reportes."""

    @abstractmethod
    def get_reporte_by_id(self, reporte_id: int) -> Optional['Reporte']:
        """Obtiene un reporte por su ID."""
        pass

    @abstractmethod
    def find_reports_by_criteria(self, criteria: dict) -> List['Reporte']:
        """Busca reportes basados en criterios (ej. tipo, rango de fechas)."""
        pass

    @abstractmethod
    def create_report_request(self, reporte: 'Reporte') -> int:
        """Crea una solicitud de reporte y devuelve el ID generado."""
        pass

    @abstractmethod
    def update_report_status(self, reporte_id: int, status: str, data: Dict = None) -> bool:
        """Actualiza el estado del reporte (COMPLETO/FALLIDO) y los datos anexos."""
        pass

class IReporteGenerador(ABC):
    """Interfaz para cualquier algoritmo o caso de uso que genere un tipo específico de reporte."""
    @abstractmethod
    def generate_report(self, **kwargs) -> Dict:
        """Ejecuta la lógica compleja y devuelve los datos estructurados del reporte."""
        pass