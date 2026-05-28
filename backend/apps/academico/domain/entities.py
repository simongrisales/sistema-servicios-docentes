from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time
from enum import StrEnum
from types import MappingProxyType
from typing import Any
from uuid import UUID

from .exceptions import (
    CampoAcademicoInvalidoError,
    CapacidadAulaInvalidaError,
    CreditosCursoInvalidosError,
    HorarioBloqueInvalidoError,
    NumeroEstudiantesInvalidoError,
)


class DiaSemana(StrEnum):
    LUNES = "lunes"
    MARTES = "martes"
    MIERCOLES = "miercoles"
    JUEVES = "jueves"
    VIERNES = "viernes"
    SABADO = "sabado"
    DOMINGO = "domingo"


class TipoAula(StrEnum):
    AULA_REGULAR = "aula_regular"
    LABORATORIO = "laboratorio"
    SALA_SISTEMAS = "sala_sistemas"
    AUDITORIO = "auditorio"


@dataclass(frozen=True, slots=True)
class Facultad:
    id: UUID
    nombre: str
    codigo: str
    activa: bool = True

    def __post_init__(self) -> None:
        _validar_texto_obligatorio(self.nombre, "nombre")
        _validar_texto_obligatorio(self.codigo, "codigo")


@dataclass(frozen=True, slots=True)
class Programa:
    id: UUID
    nombre: str
    codigo: str
    facultad_id: UUID
    activo: bool = True

    def __post_init__(self) -> None:
        _validar_texto_obligatorio(self.nombre, "nombre")
        _validar_texto_obligatorio(self.codigo, "codigo")


@dataclass(frozen=True, slots=True)
class Docente:
    id: UUID
    nombre: str
    email: str
    disponibilidad: dict[str, Any] = field(default_factory=dict)
    activo: bool = True

    def __post_init__(self) -> None:
        _validar_texto_obligatorio(self.nombre, "nombre")
        _validar_email(self.email)
        _congelar_diccionario(self, "disponibilidad", self.disponibilidad)


@dataclass(frozen=True, slots=True)
class Curso:
    id: UUID
    nombre: str
    codigo: str
    programa_id: UUID
    creditos: int
    activo: bool = True

    def __post_init__(self) -> None:
        _validar_texto_obligatorio(self.nombre, "nombre")
        _validar_texto_obligatorio(self.codigo, "codigo")
        if self.creditos <= 0:
            raise CreditosCursoInvalidosError(
                "Los creditos del curso deben ser mayores que cero."
            )


@dataclass(frozen=True, slots=True)
class Grupo:
    id: UUID
    curso_id: UUID
    docente_id: UUID
    codigo: str
    num_estudiantes: int
    semestre: str
    activo: bool = True

    def __post_init__(self) -> None:
        _validar_texto_obligatorio(self.codigo, "codigo")
        _validar_texto_obligatorio(self.semestre, "semestre")
        if self.num_estudiantes < 0:
            raise NumeroEstudiantesInvalidoError(
                "El numero de estudiantes no puede ser negativo."
            )


@dataclass(frozen=True, slots=True)
class HorarioBloque:
    id: UUID
    dia: DiaSemana
    hora_inicio: time
    hora_fin: time
    activo: bool = True

    def __post_init__(self) -> None:
        if self.hora_fin <= self.hora_inicio:
            raise HorarioBloqueInvalidoError(
                "La hora final debe ser posterior a la hora inicial."
            )


@dataclass(frozen=True, slots=True)
class GrupoHorario:
    id: UUID
    grupo_id: UUID
    horario_bloque_id: UUID


@dataclass(frozen=True, slots=True)
class Aula:
    id: UUID
    nombre: str
    capacidad: int
    tipo: TipoAula
    disponible: bool = True
    activa: bool = True

    def __post_init__(self) -> None:
        _validar_texto_obligatorio(self.nombre, "nombre")
        if self.capacidad <= 0:
            raise CapacidadAulaInvalidaError(
                "La capacidad del aula debe ser mayor que cero."
            )

    def puede_recibir(self, grupo: Grupo) -> bool:
        capacidad_suficiente = self.capacidad >= grupo.num_estudiantes
        return self.activa and self.disponible and capacidad_suficiente


@dataclass(frozen=True, slots=True)
class AulaRestriccion:
    id: UUID
    aula_id: UUID
    tipo: str
    parametros: dict[str, Any] = field(default_factory=dict)
    activa: bool = True

    def __post_init__(self) -> None:
        _validar_texto_obligatorio(self.tipo, "tipo")
        _congelar_diccionario(self, "parametros", self.parametros)


def _validar_texto_obligatorio(valor: str, campo: str) -> None:
    if not valor or not valor.strip():
        raise CampoAcademicoInvalidoError(f"El campo {campo} es obligatorio.")


def _validar_email(email: str) -> None:
    _validar_texto_obligatorio(email, "email")
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        raise CampoAcademicoInvalidoError(
            "El email del docente no tiene un formato valido."
        )


def _congelar_diccionario(
    entidad: object,
    atributo: str,
    valor: dict[str, Any],
) -> None:
    object.__setattr__(entidad, atributo, MappingProxyType(dict(valor)))
