from datetime import datetime, timedelta

import pytest

from ..application.dtos import (
    CancelarReservaInputDTO,
    ConfirmarReservaInputDTO,
    CrearReservaInputDTO,
)
from ..application.use_cases import ReservaService
from ..domain.entities import Reserva, ReservaEstado
from ..domain.exceptions import ReservaConflictoError, ReservaNoEncontradaError


def test_crear_reserva_sin_repositorio_devuelve_dto():
    service = ReservaService()
    output = service.crear_reserva(
        CrearReservaInputDTO(
            aula_id="a1",
            inicio=datetime.now(),
            fin=datetime.now() + timedelta(hours=1),
            solicitante_id="u1",
        )
    )

    assert output.aula_id == "a1"


class FakeReservaRepository:
    def __init__(self, conflicts: bool = False, reserva: Reserva | None = None) -> None:
        self.conflicts = conflicts
        self.reserva = reserva
        self.created = None
        self.updated = None

    def find_conflicts(self, aula_id, inicio, fin):
        return [self.reserva] if self.conflicts and self.reserva else []

    def crear_reserva(self, reserva):
        self.created = reserva
        return reserva

    def create(self, reserva):
        self.created = reserva
        return reserva

    def get_by_id(self, reserva_id):
        if self.reserva and self.reserva.reserva_id == reserva_id:
            return self.reserva
        return None

    def update_state(self, reserva_id, new_estado):
        self.updated = (reserva_id, new_estado)


def _reserva() -> Reserva:
    return Reserva.crear(
        reserva_id="r1",
        aula_id="a1",
        inicio=datetime.now(),
        fin=datetime.now() + timedelta(hours=1),
        solicitante_id="u1",
    )


def test_crear_reserva_rechaza_fecha_final_invalida():
    now = datetime.now()

    with pytest.raises(ReservaConflictoError, match="fecha final"):
        ReservaService().crear_reserva(
            CrearReservaInputDTO(
                aula_id="a1",
                inicio=now,
                fin=now,
                solicitante_id="u1",
            )
        )


def test_crear_reserva_rechaza_conflictos_del_repo():
    reserva = _reserva()

    with pytest.raises(ReservaConflictoError, match="ya tiene una reserva"):
        ReservaService(FakeReservaRepository(conflicts=True, reserva=reserva)).crear_reserva(
            CrearReservaInputDTO(
                aula_id="a1",
                inicio=reserva.bloque_horario_inicio,
                fin=reserva.bloque_horario_fin,
                solicitante_id="u1",
            )
        )


def test_crear_reserva_usa_metodo_transaccional_si_existe():
    repo = FakeReservaRepository(reserva=_reserva())

    output = ReservaService(repo).crear_reserva(
        CrearReservaInputDTO(
            aula_id="a1",
            inicio=datetime.now(),
            fin=datetime.now() + timedelta(hours=1),
            solicitante_id="u1",
        )
    )

    assert repo.created is not None
    assert output.estado == ReservaEstado.PENDIENTE


def test_confirmar_y_cancelar_reserva_actualizan_estado():
    repo = FakeReservaRepository(reserva=_reserva())
    service = ReservaService(repo)

    confirmada = service.confirmar_reserva(ConfirmarReservaInputDTO("r1"))
    service.cancelar_reserva(CancelarReservaInputDTO("r1"))

    assert confirmada.estado == ReservaEstado.CONFIRMADA
    assert repo.updated == ("r1", ReservaEstado.CANCELADA)


def test_confirmar_reserva_sin_repo_o_inexistente_lanza_error():
    with pytest.raises(ReservaNoEncontradaError, match="Repositorio"):
        ReservaService().confirmar_reserva(ConfirmarReservaInputDTO("r1"))

    with pytest.raises(ReservaNoEncontradaError, match="no encontrada"):
        ReservaService(FakeReservaRepository()).confirmar_reserva(
            ConfirmarReservaInputDTO("r1")
        )
