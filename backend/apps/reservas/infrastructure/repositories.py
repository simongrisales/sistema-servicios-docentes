from collections.abc import Iterable
from typing import Any

from django.utils import timezone

from core.repositories import BaseRepository

from ..domain.entities import Reserva, ReservaEstado
from ..domain.interfaces import IReservaRepository
from .models import ReservaModel


class ReservaRepository(BaseRepository[Reserva, str], IReservaRepository):
    def get(self, entity_id: str) -> Reserva | None:
        return self.get_by_id(entity_id)

    def list(self, **filters: Any) -> Iterable[Reserva]:
        return [
            self._to_domain(model) for model in ReservaModel.objects.filter(**filters)
        ]

    def create(self, data: dict[str, Any] | Reserva) -> Reserva:
        if isinstance(data, Reserva):
            return self._create_from_domain(data)
        return self._to_domain(ReservaModel.objects.create(**data))

    def update(self, entity_id: str, data: dict[str, Any]) -> Reserva:
        model = ReservaModel.objects.get(reserva_id=entity_id)
        for field, value in data.items():
            setattr(model, field, value)
        model.save(update_fields=[*data.keys()])
        return self._to_domain(model)

    def delete(self, entity_id: str) -> None:
        self.update_state(entity_id, ReservaEstado.CANCELADA)

    def get_by_id(self, reserva_id: str) -> Reserva | None:
        model = ReservaModel.objects.filter(reserva_id=reserva_id).first()
        return self._to_domain(model) if model else None

    def update_state(self, reserva_id: str, new_estado: str) -> None:
        ReservaModel.objects.filter(reserva_id=reserva_id).update(estado=new_estado)

    def find_conflicts(
        self,
        aula_id: str,
        inicio,
        fin,
    ) -> list[Reserva]:
        queryset = ReservaModel.objects.filter(
            aula_id=aula_id,
            inicio__lt=fin,
            fin__gt=inicio,
            estado__in=[ReservaEstado.PENDIENTE, ReservaEstado.CONFIRMADA],
        )
        return [self._to_domain(model) for model in queryset]

    def find_expired_reservations(self) -> list[Reserva]:
        queryset = ReservaModel.objects.filter(
            fin__lt=timezone.now(),
            estado=ReservaEstado.PENDIENTE,
        )
        return [self._to_domain(model) for model in queryset]

    def _create_from_domain(self, reserva: Reserva) -> Reserva:
        model = ReservaModel.objects.create(
            reserva_id=reserva.reserva_id,
            aula_id=reserva.aula_id,
            inicio=reserva.bloque_horario_inicio,
            fin=reserva.bloque_horario_fin,
            solicitante_id=reserva.solicitante_id,
            estado=reserva.estado,
        )
        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: ReservaModel) -> Reserva:
        return Reserva(
            reserva_id=model.reserva_id,
            aula_id=str(model.aula_id),
            bloque_horario_inicio=model.inicio,
            bloque_horario_fin=model.fin,
            solicitante_id=str(model.solicitante_id),
            estado=model.estado,
        )
