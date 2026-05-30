from collections.abc import Iterable

from ..domain.entities import Notificacion, TipoNotificacion
from ..domain.exceptions import TipoNotificacionInvalidoError
from ..domain.interfaces import INotificacionRepository
from .dtos import (
    CrearNotificacionInputDTO,
    EliminarNotificacionInputDTO,
    MarcarLeidaInputDTO,
    NotificacionOutputDTO,
)


class NotificacionService:
    """Casos de uso para enviar, listar y marcar notificaciones."""

    def __init__(self, repo: INotificacionRepository | None = None) -> None:
        self.repo = repo

    def enviar_notificacion(
        self, input_dto: CrearNotificacionInputDTO
    ) -> NotificacionOutputDTO:
        if input_dto.tipo_notificacion not in TipoNotificacion.values():
            raise TipoNotificacionInvalidoError(
                f"Tipo de notificacion no permitido: {input_dto.tipo_notificacion}"
            )

        notification = Notificacion.crear(
            tipo=input_dto.tipo_notificacion,
            titulo=input_dto.titulo,
            mensaje=input_dto.mensaje,
            destino_id=input_dto.usuario_destino_id,
        )
        if self.repo is None:
            return self._to_output(notification)
        saved_notification = self.repo.create_notification(notification)
        return self._to_output(saved_notification)

    def listar_notificaciones_no_leidas(
        self, user_id: str
    ) -> list[NotificacionOutputDTO]:
        if self.repo is None:
            return []
        return self._to_output_list(
            self.repo.get_unread_notifications_for_user(user_id)
        )

    def listar_notificaciones(self, user_id: str) -> list[NotificacionOutputDTO]:
        if self.repo is None:
            return []
        return self._to_output_list(self.repo.list_all_notifications_for_user(user_id))

    def marcar_leida(self, input_dto: MarcarLeidaInputDTO) -> bool:
        if self.repo is None:
            return False
        return self.repo.mark_as_read(input_dto.notificacion_id, input_dto.user_id)

    def eliminar_notificacion(self, input_dto: EliminarNotificacionInputDTO) -> bool:
        if self.repo is None:
            return False

        notification = self.repo.get_by_id(input_dto.notificacion_id)
        if notification is None or notification.usuario_destino_id != input_dto.user_id:
            return False

        self.repo.delete(input_dto.notificacion_id)
        return True

    def _to_output_list(
        self, notifications: Iterable[Notificacion]
    ) -> list[NotificacionOutputDTO]:
        return [self._to_output(notification) for notification in notifications]

    @staticmethod
    def _to_output(notification: Notificacion) -> NotificacionOutputDTO:
        return NotificacionOutputDTO(
            notificacion_id=notification.notificacion_id,
            titulo=notification.titulo,
            mensaje=notification.mensaje,
            fecha_creacion=notification.fecha_creacion,
            tipo=notification.tipo,
            es_leida=notification.es_leida,
        )
