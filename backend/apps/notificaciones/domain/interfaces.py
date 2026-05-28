from abc import ABC, abstractmethod
from collections.abc import Iterable

from .entities import Notificacion


class INotificacionRepository(ABC):
    """Contrato de persistencia para notificaciones."""

    @abstractmethod
    def get_by_id(self, notificacion_id: str) -> Notificacion | None:
        raise NotImplementedError

    @abstractmethod
    def create_notification(self, notification: Notificacion) -> Notificacion:
        raise NotImplementedError

    @abstractmethod
    def mark_as_read(self, notificacion_id: str, user_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_unread_notifications_for_user(self, user_id: str) -> Iterable[Notificacion]:
        raise NotImplementedError

    @abstractmethod
    def list_all_notifications_for_user(self, user_id: str) -> Iterable[Notificacion]:
        raise NotImplementedError
