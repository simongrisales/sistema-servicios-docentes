from uuid import uuid4

from django.db import transaction
from django.utils import timezone

from ..domain.entities import Reserva, ReservaEstado
from ..domain.exceptions import ReservaConflictoError, ReservaNoEncontradaError
from ..domain.interfaces import IReservaRepository
from .dtos import (
    CancelarReservaInputDTO,
    ConfirmarReservaInputDTO,
    CrearReservaInputDTO,
    ReservaOutputDTO,
)


class ReservaService:
    """Casos de uso para el ciclo de vida de reservas temporales."""

    def __init__(self, reserva_repo: IReservaRepository | None = None) -> None:
        self.reserva_repo = reserva_repo

    def crear_reserva(self, input_dto: CrearReservaInputDTO) -> ReservaOutputDTO:
        ahora = timezone.now()
        if input_dto.inicio < ahora:
            raise ReservaConflictoError(
                "La fecha de inicio no puede estar en el pasado."
            )
        if input_dto.fin <= input_dto.inicio:
            raise ReservaConflictoError("La fecha final debe ser posterior al inicio.")
        if self.reserva_repo and self.reserva_repo.find_conflicts(
            input_dto.aula_id,
            input_dto.inicio,
            input_dto.fin,
        ):
            raise ReservaConflictoError("El aula ya tiene una reserva en ese horario.")

        reserva = Reserva.crear(
            reserva_id=str(uuid4()),
            aula_id=input_dto.aula_id,
            inicio=input_dto.inicio,
            fin=input_dto.fin,
            solicitante_id=input_dto.solicitante_id,
        )
        if self.reserva_repo:
            crear_reserva = getattr(self.reserva_repo, "crear_reserva", None)
            reserva = (
                crear_reserva(reserva)
                if crear_reserva
                else self.reserva_repo.create(reserva)
            )
        return self._to_output(reserva)

    def crear_reservas_en_lote(
        self, reservas: list[CrearReservaInputDTO]
    ) -> list[ReservaOutputDTO]:
        with transaction.atomic():
            return [self.crear_reserva(reserva) for reserva in reservas]

    def confirmar_reserva(
        self, input_dto: ConfirmarReservaInputDTO
    ) -> ReservaOutputDTO:
        reserva = self._get_required(input_dto.reserva_id)
        if self.reserva_repo:
            self.reserva_repo.update_state(
                input_dto.reserva_id, ReservaEstado.CONFIRMADA
            )
        return self._to_output(
            Reserva(
                reserva.reserva_id,
                reserva.aula_id,
                reserva.bloque_horario_inicio,
                reserva.bloque_horario_fin,
                reserva.solicitante_id,
                ReservaEstado.CONFIRMADA,
            )
        )

    def cancelar_reserva(self, input_dto: CancelarReservaInputDTO) -> None:
        self._get_required(input_dto.reserva_id)
        if self.reserva_repo:
            self.reserva_repo.update_state(
                input_dto.reserva_id, ReservaEstado.CANCELADA
            )

    def _get_required(self, reserva_id: str) -> Reserva:
        if self.reserva_repo is None:
            raise ReservaNoEncontradaError("Repositorio de reservas no configurado.")
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if reserva is None:
            raise ReservaNoEncontradaError("Reserva no encontrada.")
        return reserva

    @staticmethod
    def _to_output(reserva: Reserva) -> ReservaOutputDTO:
        return ReservaOutputDTO(
            reserva_id=reserva.reserva_id,
            aula_id=reserva.aula_id,
            inicio=reserva.bloque_horario_inicio,
            fin=reserva.bloque_horario_fin,
            solicitante_id=reserva.solicitante_id,
            estado=reserva.estado,
        )
