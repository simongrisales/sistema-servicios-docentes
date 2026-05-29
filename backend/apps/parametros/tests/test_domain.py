"""Tests del dominio de parámetros (sin dependencias de Django)."""

import pytest

from ..domain.entities import CatalogoParametro
from ..domain.exceptions import CatalogoParametroInvalidoError


class TestCatalogoParametroEntity:
    def test_crea_con_todos_los_campos(self):
        p = CatalogoParametro(
            clave="max_aulas",
            valor=50,
            grupo="asignacion",
            descripcion="Máximo de aulas por semestre",
        )
        assert p.clave == "max_aulas"
        assert p.valor == 50
        assert p.activo is True

    def test_valor_puede_ser_dict(self):
        p = CatalogoParametro(
            clave="config_email",
            valor={"host": "smtp.uco.edu.co", "port": 587},
            grupo="notificaciones",
        )
        assert p.valor["port"] == 587

    def test_valor_puede_ser_lista(self):
        p = CatalogoParametro(
            clave="dias_habiles",
            valor=["lunes", "martes", "miercoles", "jueves", "viernes"],
            grupo="general",
        )
        assert len(p.valor) == 5

    def test_entidad_es_inmutable(self):
        p = CatalogoParametro(clave="k", valor=1, grupo="general")
        from dataclasses import FrozenInstanceError
        with pytest.raises(FrozenInstanceError):
            p.activo = False  # type: ignore[misc]

    def test_clave_vacia_lanza_excepcion(self):
        with pytest.raises(CatalogoParametroInvalidoError):
            CatalogoParametro(clave="", valor=1, grupo="general")

    def test_clave_solo_espacios_lanza_excepcion(self):
        with pytest.raises(CatalogoParametroInvalidoError):
            CatalogoParametro(clave="   ", valor=1, grupo="general")

    def test_grupo_invalido_lanza_excepcion(self):
        with pytest.raises(CatalogoParametroInvalidoError):
            CatalogoParametro(clave="k", valor=1, grupo="grupo_inexistente")

    def test_igualdad_por_valor(self):
        p1 = CatalogoParametro(clave="x", valor=1, grupo="general")
        p2 = CatalogoParametro(clave="x", valor=1, grupo="general")
        assert p1 == p2
