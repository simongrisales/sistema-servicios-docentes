from abc import ABC, abstractmethod
from typing import TYPE_CHECKING # Usamos tipe hints para evitar ciclos de importación

if TYPE_CHECKING:
    # Aseguramos que las entidades de dominio estén disponibles aquí solo en tiempo de chequeo.
    from ..domain.entities import Grupo, Aula, ReglaAsignacion, HorarioBloque

class IAsignacionStrategy(ABC):
    """Interfaz concreta para todas las estrategias de asignación."""
    @abstractmethod
    def __init__(self, reglas: List['ReglaAsignacion']):
        """Inicializa la estrategia con el conjunto de reglas de negocio activas."""
        pass

    @abstractmethod
    def seleccionar_mejor_aula(self, grupo: 'Grupo', horario_bloque: 'HorarioBloque') -> Aula:
        """Implementa la lógica de scoring para determinar la aula óptima."""
        pass