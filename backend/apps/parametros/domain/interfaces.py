"""Interfaces (contratos) del dominio de parámetros.

Define los puertos de salida (repositorios) que la capa de infraestructura
debe implementar. Sin imports de Django — Python puro.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

from .entities import CatalogoParametro


class ICatalogoParametroRepository(ABC):
    """Contrato para el repositorio de parámetros del catálogo."""

    @abstractmethod
    def obtener(self, clave: str) -> CatalogoParametro | None:
        """Recupera un parámetro por su clave única."""
        raise NotImplementedError

    @abstractmethod
    def listar(self, grupo: str | None = None) -> Iterable[CatalogoParametro]:
        """Lista todos los parámetros, opcionalmente filtrados por grupo."""
        raise NotImplementedError

    @abstractmethod
    def guardar(self, parametro: CatalogoParametro) -> CatalogoParametro:
        """Crea o actualiza un parámetro. Retorna la entidad persistida."""
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, clave: str) -> None:
        """Elimina un parámetro por su clave."""
        raise NotImplementedError

    @abstractmethod
    def obtener_valor(self, clave: str, default: Any = None) -> Any:
        """Atajo para leer sólo el valor de un parámetro (con fallback)."""
        raise NotImplementedError
