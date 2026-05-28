from abc import ABC, abstractmethod
from datetime import datetime

from .entities import Reserva


class IReservaRepository(ABC):
    @abstractmethod
    def get_by_id(self, reserva_id: str) -> Reserva | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, reserva: Reserva) -> Reserva:
        raise NotImplementedError

    @abstractmethod
    def update_state(self, reserva_id: str, new_estado: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_conflicts(
        self,
        aula_id: str,
        inicio: datetime,
        fin: datetime,
    ) -> list[Reserva]:
        raise NotImplementedError

    @abstractmethod
    def find_expired_reservations(self) -> list[Reserva]:
        raise NotImplementedError
