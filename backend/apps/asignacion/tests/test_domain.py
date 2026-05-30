"""Tests de la capa de dominio de asignacion (sin dependencias de Django)."""

import pytest

from ..domain.entities import Asignacion, ReglaAsignacion, ResultadoAsignacion
from ..domain.exceptions import (
    AsignacionConflictoError,
    CapacidadInsuficienteError,
    DatosIncompletosError,
    SinAulasDisponiblesError,
)
from ..infrastructure.strategies import PrioridadEstudiantesStrategy

# ---------------------------------------------------------------------------
# Entidad Asignacion
# ---------------------------------------------------------------------------


class TestAsignacionEntity:
    def test_conserva_todos_los_campos(self):
        asignacion = Asignacion(
            id=1,
            grupo_id=10,
            aula_id=20,
            bloque_horario_id=30,
            semestre="2026-1",
            estado="CONFIRMADO",
        )
        assert asignacion.id == 1
        assert asignacion.grupo_id == 10
        assert asignacion.aula_id == 20
        assert asignacion.bloque_horario_id == 30
        assert asignacion.semestre == "2026-1"
        assert asignacion.estado == "CONFIRMADO"

    def test_entidad_frozen_inmutable(self):
        asignacion = Asignacion(
            id=1,
            grupo_id=2,
            aula_id=3,
            bloque_horario_id=4,
            semestre="2026-1",
            estado="PENDIENTE",
        )
        from dataclasses import FrozenInstanceError

        with pytest.raises(FrozenInstanceError):
            asignacion.estado = "MODIFICADO"  # type: ignore[misc]

    def test_igualdad_por_valor(self):
        a1 = Asignacion(
            id=1,
            grupo_id=2,
            aula_id=3,
            bloque_horario_id=4,
            semestre="2026-1",
            estado="CONFIRMADO",
        )
        a2 = Asignacion(
            id=1,
            grupo_id=2,
            aula_id=3,
            bloque_horario_id=4,
            semestre="2026-1",
            estado="CONFIRMADO",
        )
        assert a1 == a2


# ---------------------------------------------------------------------------
# Entidad ReglaAsignacion
# ---------------------------------------------------------------------------


class TestReglaAsignacionEntity:
    def test_activa_por_defecto(self):
        regla = ReglaAsignacion(nombre="R1", tipo="CAPACIDAD", parametros={})
        assert regla.activa is True

    def test_inactiva_cuando_se_especifica(self):
        regla = ReglaAsignacion(
            nombre="R2", tipo="HORARIO", parametros={"max": 5}, activa=False
        )
        assert regla.activa is False


# ---------------------------------------------------------------------------
# Entidad ResultadoAsignacion
# ---------------------------------------------------------------------------


class TestResultadoAsignacionEntity:
    def test_exitoso_sin_conflictos(self):
        resultado = ResultadoAsignacion(exitoso=True, mensaje="OK")
        assert resultado.exitoso is True
        assert resultado.conflicto_detalles == []
        assert resultado.aula_sugerida_id is None

    def test_fallido_con_conflictos(self):
        resultado = ResultadoAsignacion(
            exitoso=False,
            mensaje="Conflicto",
            aula_sugerida_id=99,
            conflicto_detalles=["Aula ocupada"],
        )
        assert resultado.exitoso is False
        assert len(resultado.conflicto_detalles) == 1
        assert resultado.aula_sugerida_id == 99


# ---------------------------------------------------------------------------
# Excepciones de dominio
# ---------------------------------------------------------------------------


class TestDomainExceptions:
    def test_asignacion_conflicto_error_guarda_detalles(self):
        err = AsignacionConflictoError(["Detalle 1", "Detalle 2"])
        assert len(err.detalles_conflicto) == 2
        assert "Detalle 1" in err.detalles_conflicto

    def test_asignacion_conflicto_error_mensaje_personalizado(self):
        err = AsignacionConflictoError([], mensaje="Error personalizado")
        assert str(err) == "Error personalizado"

    def test_capacidad_insuficiente_error(self):
        err = CapacidadInsuficienteError("Sin espacio")
        assert isinstance(err, Exception)

    def test_sin_aulas_disponibles_error(self):
        err = SinAulasDisponiblesError("No hay aulas")
        assert isinstance(err, Exception)

    def test_datos_incompletos_error(self):
        err = DatosIncompletosError("Faltan datos")
        assert isinstance(err, Exception)


class TestPrioridadEstudiantesStrategy:
    def test_ordena_grupos_de_mayor_a_menor(self):
        strategy = PrioridadEstudiantesStrategy()
        resultado = strategy.asignar(
            grupos=[
                {
                    "id": "g1",
                    "num_estudiantes": 10,
                    "bloque_horario_id": "b1",
                    "semestre": "2026-1",
                },
                {
                    "id": "g2",
                    "num_estudiantes": 30,
                    "bloque_horario_id": "b1",
                    "semestre": "2026-1",
                },
            ],
            aulas=[
                {"id": "a1", "capacidad": 20, "disponible": True, "activa": True},
                {"id": "a2", "capacidad": 40, "disponible": True, "activa": True},
            ],
            reglas=[],
        )

        assert resultado.exitoso is True
        assert resultado.asignaciones[0]["grupo_id"] == "g2"

    def test_detecta_conflicto_de_horario(self):
        strategy = PrioridadEstudiantesStrategy()
        resultado = strategy.asignar(
            grupos=[
                {
                    "id": "g1",
                    "num_estudiantes": 20,
                    "bloque_horario_id": "b1",
                    "semestre": "2026-1",
                },
                {
                    "id": "g2",
                    "num_estudiantes": 15,
                    "bloque_horario_id": "b1",
                    "semestre": "2026-1",
                },
            ],
            aulas=[
                {"id": "a1", "capacidad": 25, "disponible": True, "activa": True},
            ],
            reglas=[],
        )

        assert resultado.exitoso is False
        assert resultado.conflicto_detalles

    def test_usa_el_aula_mas_pequena_que_alcanza(self):
        strategy = PrioridadEstudiantesStrategy()
        resultado = strategy.asignar(
            grupos=[
                {
                    "id": "g1",
                    "num_estudiantes": 18,
                    "bloque_horario_id": "b1",
                    "semestre": "2026-1",
                }
            ],
            aulas=[
                {"id": "a1", "capacidad": 30, "disponible": True, "activa": True},
                {"id": "a2", "capacidad": 20, "disponible": True, "activa": True},
                {"id": "a3", "capacidad": 50, "disponible": True, "activa": True},
            ],
            reglas=[],
        )

        assert resultado.exitoso is True
        assert resultado.asignaciones[0]["aula_id"] == "a2"

    def test_marca_pendiente_si_no_hay_aula(self):
        strategy = PrioridadEstudiantesStrategy()
        resultado = strategy.asignar(
            grupos=[
                {
                    "id": "g1",
                    "num_estudiantes": 20,
                    "bloque_horario_id": "b1",
                    "semestre": "2026-1",
                }
            ],
            aulas=[
                {"id": "a1", "capacidad": 10, "disponible": True, "activa": True},
            ],
            reglas=[],
        )

        assert resultado.exitoso is False
        assert resultado.asignaciones[0]["estado"] == "PENDIENTE"
