from abc import ABC, abstractmethod
from collections.abc import Iterable
from uuid import UUID

from .entities import (
    Aula,
    Curso,
    Docente,
    Facultad,
    Grupo,
    HorarioBloque,
    Programa,
)


class IFacultadRepository(ABC):
    @abstractmethod
    def get(self, facultad_id: UUID) -> Facultad | None:
        raise NotImplementedError

    @abstractmethod
    def list_activas(self) -> Iterable[Facultad]:
        raise NotImplementedError


class IProgramaRepository(ABC):
    @abstractmethod
    def get(self, programa_id: UUID) -> Programa | None:
        raise NotImplementedError

    @abstractmethod
    def list_por_facultad(self, facultad_id: UUID) -> Iterable[Programa]:
        raise NotImplementedError


class IDocenteRepository(ABC):
    @abstractmethod
    def get(self, docente_id: UUID) -> Docente | None:
        raise NotImplementedError

    @abstractmethod
    def get_por_email(self, email: str) -> Docente | None:
        raise NotImplementedError


class ICursoRepository(ABC):
    @abstractmethod
    def get(self, curso_id: UUID) -> Curso | None:
        raise NotImplementedError

    @abstractmethod
    def list_por_programa(self, programa_id: UUID) -> Iterable[Curso]:
        raise NotImplementedError


class IGrupoRepository(ABC):
    @abstractmethod
    def get(self, grupo_id: UUID) -> Grupo | None:
        raise NotImplementedError

    @abstractmethod
    def list_por_semestre(self, semestre: str) -> Iterable[Grupo]:
        raise NotImplementedError

    @abstractmethod
    def list_por_curso(self, curso_id: UUID) -> Iterable[Grupo]:
        raise NotImplementedError


class IHorarioBloqueRepository(ABC):
    @abstractmethod
    def get(self, horario_bloque_id: UUID) -> HorarioBloque | None:
        raise NotImplementedError

    @abstractmethod
    def list_activos(self) -> Iterable[HorarioBloque]:
        raise NotImplementedError


class IAulaRepository(ABC):
    @abstractmethod
    def get(self, aula_id: UUID) -> Aula | None:
        raise NotImplementedError

    @abstractmethod
    def list_disponibles(self) -> Iterable[Aula]:
        raise NotImplementedError

    @abstractmethod
    def list_con_capacidad_minima(self, capacidad_minima: int) -> Iterable[Aula]:
        raise NotImplementedError
