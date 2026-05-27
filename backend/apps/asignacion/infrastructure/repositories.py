from abc import ABC, abstractmethod
from typing import List
from ..domain.entities import Grupo, Aula, HorarioBloque

# Importaciones de Modelos ORM para la implementación
from .models import *


class BaseRepository(ABC):
    """Clase base que proporciona métodos CRUD genéricos y transaccionales."""
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Any]: pass

# --- Implementación Concreta del Repositorio de Asignaciones ---
class AcademicoRepository(BaseRepository):
    """Implementa la lógica de persistencia usando el ORM de Django."""

    def __init__(self, grupo_repo=None, aula_repo=None):
        # Inicializar con repositorios dependientes (mockeados o reales)
        pass

    @abstractmethod
    def get_grupo(self, grupo_id: int) -> Optional[Grupo]:
        """Implementación de IGrupoRepository.get_grupo."""
        # Aquí se consultaría GrupoModel para mapearlo a Grupo entidad
        return None # Placeholder

    def find_aulas_por_bloque(self, horario_bloque: HorarioBloque) -> List[Aula]:
        """Implementación de IAulaRepository.find_aulas_por_bloque."""
        # Consulta compleja que utiliza filtros transaccionales en el ORM
        try:
            # Lógica real usando django.db.transaction y select_related
            pass
        except Exception as e:
            print(f"Error de DB al buscar aulas disponibles: {e}")
            return []

    @abstractmethod
    def crear_asignacion_transaccional(self, grupo_id: int, aula_id: int, bloque_horario: HorarioBloque) -> bool:
        """Método transaccional para garantizar la integridad de datos."""
        # Esta función debe envolver lógica ORM con @transaction.atomic en el modelo AsignacionModel

        # ... Lógica transaccional a implementar ...
        pass