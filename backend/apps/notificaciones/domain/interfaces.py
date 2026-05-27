# backend/apps/notificaciones/domain/interfaces.py

from abc import ABC, abstractmethod
from typing import List, Optional
from sistemaserviciosdocentes.backend.apps.notificaciones.domain.entities import Notificacion
from datetime import datetime

class INotificacionRepository(ABC):
    """
    Interfaz de repositorio para la capa de Notificaciones.
    Define el contrato abstracto para todas las operaciones de persistencia.
    """

    @abstractmethod
    def get_by_id(self, notificacion_id: str) -> Optional[Notificacion]:
        """Obtiene una notificación por su ID."""
        pass

    @abstractmethod
    def create_notification(self, notification: Notificacion) -> None:
        """Persiste una nueva notificación en el sistema."""
        pass

    @abstractmethod
    def mark_as_read(self, notificacion_id: str, user_id: str) -> bool:
        """Marca la notificación como leída para un usuario específico."""
        pass

    @abstractmethod
    def get_unread_notifications_for_user(self, user_id: str) -> List[Notificacion]:
        """Recupera todas las notificaciones no leídas y ordenadas por fecha."""
        pass

    @abstractmethod
    def list_all_notifications_for_user(self, user_id: str) -> List[Notificacion]:
        """Lista el historial completo de notificaciones para un usuario."""
        pass