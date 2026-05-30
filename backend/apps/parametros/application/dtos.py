"""DTOs de la capa de aplicación de parámetros."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ParametroInputDTO:
    """Datos de entrada para crear o actualizar un parámetro."""

    clave: str
    valor: Any
    grupo: str = "general"
    descripcion: str = ""
    activo: bool = True


@dataclass(frozen=True)
class ParametroOutputDTO:
    """Datos de salida de un parámetro del catálogo."""

    clave: str
    valor: Any
    grupo: str
    descripcion: str
    activo: bool


@dataclass(frozen=True)
class ObtenerValorInputDTO:
    """Parámetros para consultar el valor de una clave."""

    clave: str
    default: Any = None
