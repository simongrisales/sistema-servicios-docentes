import pytest

from apps.notificaciones.application.dtos import (
    CrearNotificacionInputDTO,
    MarcarLeidaInputDTO,
)
from apps.notificaciones.application.use_cases import NotificacionService
from apps.notificaciones.domain.entities import Notificacion, TipoNotificacion
from apps.notificaciones.domain.exceptions import TipoNotificacionInvalidoError


def test_tipos_de_notificacion_incluyen_los_canonicos():
    values = TipoNotificacion.values()

    assert TipoNotificacion.ASIGNACION_COMPLETADA in values
    assert TipoNotificacion.CONFLICTO_DETECTADO in values
    assert TipoNotificacion.RESERVA_CONFIRMADA in values
    assert TipoNotificacion.RESERVA_EXPIRADA in values


class FakeNotificacionRepository:
    def __init__(self) -> None:
        self.notification = Notificacion.crear(
            tipo=TipoNotificacion.CONFLICTO_DETECTADO,
            titulo="Conflicto",
            mensaje="Aula ocupada",
            destino_id="7",
            notification_id="n1",
        )
        self.marked = None

    def create_notification(self, notification):
        return Notificacion(
            notificacion_id="n2",
            tipo=notification.tipo,
            titulo=notification.titulo,
            mensaje=notification.mensaje,
            fecha_creacion=notification.fecha_creacion,
            usuario_destino_id=notification.usuario_destino_id,
        )

    def get_unread_notifications_for_user(self, user_id: str):
        return [self.notification] if user_id == "7" else []

    def list_all_notifications_for_user(self, user_id: str):
        return [self.notification] if user_id == "7" else []

    def mark_as_read(self, notificacion_id: str, user_id: str):
        self.marked = (notificacion_id, user_id)
        return True


def test_enviar_notificacion_sin_repo_devuelve_output():
    output = NotificacionService().enviar_notificacion(
        CrearNotificacionInputDTO(
            titulo="Asignacion lista",
            mensaje="Proceso terminado",
            tipo_notificacion=TipoNotificacion.ASIGNACION_COMPLETADA,
            usuario_destino_id="1",
        )
    )

    assert output.tipo == TipoNotificacion.ASIGNACION_COMPLETADA
    assert output.es_leida is False


def test_enviar_notificacion_tipo_invalido_lanza_error():
    with pytest.raises(TipoNotificacionInvalidoError):
        NotificacionService().enviar_notificacion(
            CrearNotificacionInputDTO(
                titulo="X",
                mensaje="Y",
                tipo_notificacion="tipo_invalido",
                usuario_destino_id="1",
            )
        )


def test_listar_y_marcar_notificaciones_con_repo():
    repo = FakeNotificacionRepository()
    service = NotificacionService(repo)

    unread = service.listar_notificaciones_no_leidas("7")
    all_notifications = service.listar_notificaciones("7")
    marked = service.marcar_leida(MarcarLeidaInputDTO("n1", "7"))

    assert unread[0].notificacion_id == "n1"
    assert all_notifications[0].titulo == "Conflicto"
    assert marked is True
    assert repo.marked == ("n1", "7")


def test_notificaciones_sin_repo_devuelven_valores_neutros():
    service = NotificacionService()

    assert service.listar_notificaciones_no_leidas("7") == []
    assert service.listar_notificaciones("7") == []
    assert service.marcar_leida(MarcarLeidaInputDTO("n1", "7")) is False
