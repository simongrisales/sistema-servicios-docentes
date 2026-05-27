from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities import Aula, Grupo, Docente, Curso, HorarioBloque

class IRepository(ABC):
    """Contrato base para la capa de repositorio del módulo Asignación."""
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Any]:
        pass

# --- Contratos de Repositorios Dependientes (Se asumen existencias en otros módulos) ---

class IGrupoRepository(ABC):
    """Contrato para acceder a la información de los Grupos."""
    @abstractmethod
    def get_grupo(self, grupo_id: int) -> Optional[Grupo]: pass

class IAulaRepository(ABC):
    """Contrato para buscar y gestionar aulas disponibles."""
    @abstractmethod
    def find_aulas_por_bloque(self, horario_bloque: HorarioBloque) -> List[Aula]: pass

# --- Contratos de Estrategia (Patrón Strategy) ---

class IAsignacionStrategy(ABC):
    """Interfaz para todas las estrategias de asignación de aulas."""
    @abstractmethod
    def __init__(self, reglas: list['ReglaAsignacion']):
        pass

    @abstractmethod
    def calcular_puntuacion_aula(self, aula: Aula, grupo: Grupo) -> int:
        """Calcula una puntuación basada en las reglas de negocio (más alta es mejor)."""
        pass

# --- Contratos para otras dependencias ---

class IReglaRepository(ABC):
    """Contrato para consultar y gestionar las Reglas de Negocio."""
    @abstractmethod
    def obtener_reglas_activas(self) -> List['ReglaAsignacion']: pass