from abc import ABC, abstractmethod
from collections.abc import Iterable

from .entities import Asignacion, ReglaAsignacion, ResultadoAsignacion


class IAsignacionRepository(ABC):
    @abstractmethod
    def existe_conflicto(
        self, aula_id: str, bloque_horario_id: str, semestre: str
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def guardar(self, asignacion: Asignacion) -> Asignacion:
        raise NotImplementedError

    @abstractmethod
    def listar_por_semestre(self, semestre: str) -> Iterable[Asignacion]:
        raise NotImplementedError

    @abstractmethod
    def contar_grupos_por_semestre(self, semestre: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def contar_grupos_asignados_por_semestre(self, semestre: str) -> int:
        raise NotImplementedError


class IAsignacionStrategy(ABC):
    @abstractmethod
    def asignar(
        self,
        grupos: list[dict],
        aulas: list[dict],
        reglas: list[ReglaAsignacion],
    ) -> ResultadoAsignacion:
        raise NotImplementedError
