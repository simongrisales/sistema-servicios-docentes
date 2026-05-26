from dataclasses import dataclass
from typing import List, Optional
from .entities import Aula, Grupo, Docente, Curso

# DTOs para la carga masiva y creación/actualización de grupos
@dataclass(frozen=True)
class CargaMasivaInputDTO:
    """Datos batch para crear múltiples Grupos."""
    grupo_id: int
    curso_id: int
    docente_id: int
    num_estudiantes: int # Estudiantes iniciales

@dataclass(frozen=True)
class GrupoInputDTO:
    """DTO de entrada para la creación/actualización de un único grupo."""
    grupo_id: Optional[int] = None
    curso_id: int
    docente_id: int
    num_estudiantes: int

@dataclass(frozen=True)
class AulaInputDTO:
    """DTO de entrada para la creación/actualización de un aula."""
    aula_id: Optional[int] = None
    nombre: str
    capacidad: int
    tipo: str
    disponible: bool

# DTOs de salida (Output)
@dataclass(frozen=True)
class GrupoOutputDTO:
    """Representación de un grupo después de ser creado o actualizado."""
    grupo_id: int
    curso_id: int
    docente_id: int
    num_estudiantes: int

@dataclass(frozen=True)
class AulaOutputDTO:
    """Representación de una aula disponible."""
    aula_id: int
    nombre: str
    capacidad: int
    tipo: str
    disponible: bool
