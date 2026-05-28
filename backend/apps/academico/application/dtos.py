from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AulaInputDTO:
    nombre: str
    capacidad: int
    tipo: str
    disponible: bool = True


@dataclass(frozen=True)
class AulaOutputDTO:
    id: UUID | None
    nombre: str
    capacidad: int
    tipo: str
    disponible: bool


@dataclass(frozen=True)
class GrupoInputDTO:
    curso_id: UUID
    docente_id: UUID
    codigo: str
    num_estudiantes: int
    semestre: str


@dataclass(frozen=True)
class GrupoOutputDTO:
    id: UUID | None
    curso_id: UUID
    docente_id: UUID
    codigo: str
    num_estudiantes: int
    semestre: str


@dataclass(frozen=True)
class DocenteInputDTO:
    nombre: str
    email: str


@dataclass(frozen=True)
class DocenteOutputDTO:
    id: UUID | None
    nombre: str
    email: str


@dataclass(frozen=True)
class CargaMasivaInputDTO:
    grupos: list[GrupoInputDTO]
