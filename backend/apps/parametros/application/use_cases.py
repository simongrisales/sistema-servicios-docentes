"""Casos de uso de la app parametros.

Orquestan el dominio sin acoplarse a Django ni a la BD.
"""

from collections.abc import Iterable
from typing import Any

from ..domain.entities import CatalogoParametro
from ..domain.exceptions import (
    CatalogoParametroDuplicadoError,
    CatalogoParametroNoEncontradoError,
)
from ..domain.interfaces import ICatalogoParametroRepository
from .dtos import ObtenerValorInputDTO, ParametroInputDTO, ParametroOutputDTO


def _to_output(parametro: CatalogoParametro) -> ParametroOutputDTO:
    return ParametroOutputDTO(
        clave=parametro.clave,
        valor=parametro.valor,
        grupo=parametro.grupo,
        descripcion=parametro.descripcion,
        activo=parametro.activo,
    )


class CatalogoParametroService:
    """Servicio de aplicación para el catálogo de parámetros del sistema."""

    def __init__(
        self, repo: ICatalogoParametroRepository | None = None
    ) -> None:
        self._repo = repo

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def obtener(self, clave: str) -> ParametroOutputDTO:
        """Obtiene un parámetro por clave. Lanza excepción si no existe."""
        if self._repo is None:
            raise CatalogoParametroNoEncontradoError(
                "Repositorio no configurado."
            )
        parametro = self._repo.obtener(clave)
        if parametro is None:
            raise CatalogoParametroNoEncontradoError(
                f"No existe el parámetro '{clave}'."
            )
        return _to_output(parametro)

    def listar(
        self, grupo: str | None = None
    ) -> Iterable[ParametroOutputDTO]:
        """Lista todos los parámetros, opcionalmente filtrados por grupo."""
        if self._repo is None:
            return []
        return [_to_output(p) for p in self._repo.listar(grupo=grupo)]

    def obtener_valor(self, dto: ObtenerValorInputDTO) -> Any:
        """Retorna sólo el valor de un parámetro, con default si no existe."""
        if self._repo is None:
            return dto.default
        return self._repo.obtener_valor(dto.clave, dto.default)

    # ------------------------------------------------------------------
    # Comandos
    # ------------------------------------------------------------------

    def crear(self, dto: ParametroInputDTO) -> ParametroOutputDTO:
        """Crea un nuevo parámetro. Falla si la clave ya existe."""
        if self._repo is None:
            # Sin repositorio: simula creación en memoria
            parametro = CatalogoParametro(
                clave=dto.clave,
                valor=dto.valor,
                grupo=dto.grupo,
                descripcion=dto.descripcion,
                activo=dto.activo,
            )
            return _to_output(parametro)

        if self._repo.obtener(dto.clave) is not None:
            raise CatalogoParametroDuplicadoError(
                f"Ya existe el parámetro '{dto.clave}'."
            )

        parametro = CatalogoParametro(
            clave=dto.clave,
            valor=dto.valor,
            grupo=dto.grupo,
            descripcion=dto.descripcion,
            activo=dto.activo,
        )
        return _to_output(self._repo.guardar(parametro))

    def actualizar(self, dto: ParametroInputDTO) -> ParametroOutputDTO:
        """Actualiza un parámetro existente. Falla si no existe."""
        if self._repo is None:
            raise CatalogoParametroNoEncontradoError(
                "Repositorio no configurado."
            )
        existing = self._repo.obtener(dto.clave)
        if existing is None:
            raise CatalogoParametroNoEncontradoError(
                f"No existe el parámetro '{dto.clave}'."
            )
        parametro = CatalogoParametro(
            clave=dto.clave,
            valor=dto.valor,
            grupo=dto.grupo,
            descripcion=dto.descripcion,
            activo=dto.activo,
        )
        return _to_output(self._repo.guardar(parametro))

    def eliminar(self, clave: str) -> None:
        """Elimina un parámetro. Falla si no existe."""
        if self._repo is None:
            raise CatalogoParametroNoEncontradoError(
                "Repositorio no configurado."
            )
        if self._repo.obtener(clave) is None:
            raise CatalogoParametroNoEncontradoError(
                f"No existe el parámetro '{clave}'."
            )
        self._repo.eliminar(clave)
