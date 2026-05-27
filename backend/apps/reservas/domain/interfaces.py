from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Reserva

class IReservaRepository(ABC):
    """
    Interfaz de repositorio para la capa de Reservas. Define el contrato
    para persistir y consultar entidades de reserva sin depender del ORM.
    """

    @abstractmethod
    def get_by_id(self, reserva_id: str) -> Optional[Reserva]:
        """Obtiene una Reserva por su ID."""
        pass

    @abstractmethod
    def create(self, reserva: Reserva) -> None:
        """Persiste una nueva Reserva en el sistema (transacción atómica)."""
        pass

    @abstractmethod
    def update_state(self, reserva_id: str, new_estado: str) -> None:
        """Actualiza el estado de la reserva."""
        pass

    @abstractmethod
    def find_conflicts(self, aula_id: str, inicio: datetime, fin: datetime) -> List[Reserva]:
        """
        Busca todas las reservas activas que se superponen con un bloque horario dado
        para una aula específica. Esta es la función CRÍTICA de validación de conflictos.
        """
        pass

    @abstractmethod
    def find_expired_reservations(self) -> List[Reserva]:
        """Recupera todas las reservas cuyo estado debe ser marcado como expirado."""
        pass