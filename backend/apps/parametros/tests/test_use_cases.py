"""Tests de los casos de uso de parámetros (con mocks de repositorio)."""

from unittest.mock import MagicMock

import pytest

from ..application.dtos import ObtenerValorInputDTO, ParametroInputDTO
from ..application.use_cases import CatalogoParametroService
from ..domain.entities import CatalogoParametro
from ..domain.exceptions import (
    CatalogoParametroDuplicadoError,
    CatalogoParametroNoEncontradoError,
)


def _make_parametro(clave: str = "k1", valor=42, grupo: str = "general"):
    return CatalogoParametro(clave=clave, valor=valor, grupo=grupo)


# ---------------------------------------------------------------------------
# Listar y obtener
# ---------------------------------------------------------------------------


class TestListarParametros:
    def test_listar_sin_repo_devuelve_lista_vacia(self):
        service = CatalogoParametroService()
        assert list(service.listar()) == []

    def test_listar_con_repo_devuelve_todos(self):
        repo = MagicMock()
        repo.listar.return_value = [_make_parametro("k1"), _make_parametro("k2")]
        service = CatalogoParametroService(repo)

        result = list(service.listar())
        assert len(result) == 2
        assert result[0].clave == "k1"

    def test_listar_filtra_por_grupo(self):
        repo = MagicMock()
        repo.listar.return_value = []
        service = CatalogoParametroService(repo)

        service.listar(grupo="asignacion")
        repo.listar.assert_called_once_with(grupo="asignacion")


class TestObtenerParametro:
    def test_obtener_sin_repo_lanza_excepcion(self):
        service = CatalogoParametroService()
        with pytest.raises(CatalogoParametroNoEncontradoError):
            service.obtener("cualquier_clave")

    def test_obtener_existente_devuelve_output_dto(self):
        repo = MagicMock()
        repo.obtener.return_value = _make_parametro("mi_clave", valor=99)
        service = CatalogoParametroService(repo)

        output = service.obtener("mi_clave")
        assert output.clave == "mi_clave"
        assert output.valor == 99

    def test_obtener_inexistente_lanza_excepcion(self):
        repo = MagicMock()
        repo.obtener.return_value = None
        service = CatalogoParametroService(repo)

        with pytest.raises(CatalogoParametroNoEncontradoError):
            service.obtener("no_existe")


class TestObtenerValor:
    def test_obtener_valor_sin_repo_retorna_default(self):
        service = CatalogoParametroService()
        result = service.obtener_valor(ObtenerValorInputDTO(clave="x", default=99))
        assert result == 99

    def test_obtener_valor_con_repo(self):
        repo = MagicMock()
        repo.obtener_valor.return_value = 42
        service = CatalogoParametroService(repo)

        result = service.obtener_valor(ObtenerValorInputDTO(clave="x", default=0))
        assert result == 42


# ---------------------------------------------------------------------------
# Crear
# ---------------------------------------------------------------------------


class TestCrearParametro:
    def test_crear_sin_repo_simula_en_memoria(self):
        service = CatalogoParametroService()
        dto = ParametroInputDTO(clave="nuevo", valor="hola", grupo="general")
        output = service.crear(dto)
        assert output.clave == "nuevo"
        assert output.valor == "hola"

    def test_crear_con_repo_guarda(self):
        repo = MagicMock()
        repo.obtener.return_value = None
        repo.guardar.return_value = _make_parametro("nuevo", valor="hola")
        service = CatalogoParametroService(repo)

        dto = ParametroInputDTO(clave="nuevo", valor="hola", grupo="general")
        output = service.crear(dto)
        repo.guardar.assert_called_once()
        assert output.clave == "nuevo"

    def test_crear_duplicado_lanza_excepcion(self):
        repo = MagicMock()
        repo.obtener.return_value = _make_parametro("existente")
        service = CatalogoParametroService(repo)

        with pytest.raises(CatalogoParametroDuplicadoError):
            service.crear(
                ParametroInputDTO(clave="existente", valor=1, grupo="general")
            )


# ---------------------------------------------------------------------------
# Eliminar
# ---------------------------------------------------------------------------


class TestEliminarParametro:
    def test_eliminar_inexistente_lanza_excepcion(self):
        repo = MagicMock()
        repo.obtener.return_value = None
        service = CatalogoParametroService(repo)

        with pytest.raises(CatalogoParametroNoEncontradoError):
            service.eliminar("no_existe")

    def test_eliminar_existente_llama_repo(self):
        repo = MagicMock()
        repo.obtener.return_value = _make_parametro("a_borrar")
        service = CatalogoParametroService(repo)

        service.eliminar("a_borrar")
        repo.eliminar.assert_called_once_with("a_borrar")
