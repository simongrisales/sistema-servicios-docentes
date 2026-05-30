from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from apps.notificaciones.application.dtos import (
    CrearNotificacionInputDTO,
    EliminarNotificacionInputDTO,
    MarcarLeidaInputDTO,
)
from apps.notificaciones.application.use_cases import NotificacionService
from apps.notificaciones.domain.entities import Notificacion, TipoNotificacion
from apps.notificaciones.domain.exceptions import TipoNotificacionInvalidoError
from apps.notificaciones.infrastructure.consumers import (
    DisponibilidadAulaConsumer,
    NotificacionConsumer,
    PanelSyncConsumer,
    ProgresoAsignacionConsumer,
)


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
        self.deleted = None

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

    def delete(self, notificacion_id: str):
        self.deleted = notificacion_id

    def get_by_id(self, notificacion_id: str):
        if self.notification.notificacion_id == notificacion_id:
            return self.notification
        return None


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
    service = NotificacionService()

    try:
        service.enviar_notificacion(
            CrearNotificacionInputDTO(
                titulo="X",
                mensaje="Y",
                tipo_notificacion="tipo_invalido",
                usuario_destino_id="1",
            )
        )
    except TipoNotificacionInvalidoError:
        assert True
    else:
        raise AssertionError("Se esperaba TipoNotificacionInvalidoError")


def test_listar_y_marcar_notificaciones_con_repo():
    repo = FakeNotificacionRepository()
    service = NotificacionService(repo)

    output = service.enviar_notificacion(
        CrearNotificacionInputDTO(
            titulo="Asignacion lista",
            mensaje="Ya fue publicada",
            tipo_notificacion=TipoNotificacion.ASIGNACION_COMPLETADA,
            usuario_destino_id="7",
        )
    )
    unread = service.listar_notificaciones_no_leidas("7")
    all_notifications = service.listar_notificaciones("7")
    marked = service.marcar_leida(MarcarLeidaInputDTO("n1", "7"))

    assert output.notificacion_id == "n2"
    assert output.tipo == TipoNotificacion.ASIGNACION_COMPLETADA
    assert unread[0].notificacion_id == "n1"
    assert all_notifications[0].titulo == "Conflicto"
    assert marked is True
    assert repo.marked == ("n1", "7")


def test_eliminar_notificacion_con_repo():
    repo = FakeNotificacionRepository()
    service = NotificacionService(repo)

    deleted = service.eliminar_notificacion(
        EliminarNotificacionInputDTO("n1", "7")
    )

    assert deleted is True
    assert repo.deleted == "n1"


def test_notificaciones_sin_repo_devuelven_valores_neutros():
    service = NotificacionService()

    assert service.listar_notificaciones_no_leidas("7") == []
    assert service.listar_notificaciones("7") == []
    assert service.marcar_leida(MarcarLeidaInputDTO("n1", "7")) is False


class NotificacionConsumerTests(IsolatedAsyncioTestCase):
    async def test_connect_rechaza_usuario_anonimo(self):
        consumer = NotificacionConsumer()
        consumer.scope = {"user": SimpleNamespace(is_authenticated=False)}
        consumer.close = AsyncMock()

        await consumer.connect()

        consumer.close.assert_awaited_once_with(code=4401)

    async def test_connect_asigna_grupo_y_acepta_usuario_autenticado(self):
        consumer = NotificacionConsumer()
        consumer.scope = {
            "user": SimpleNamespace(is_authenticated=True, pk=7),
        }
        consumer.channel_layer = AsyncMock()
        consumer.channel_name = "channel-1"
        consumer.accept = AsyncMock()

        await consumer.connect()

        consumer.channel_layer.group_add.assert_awaited_once_with(
            "notificaciones_usuario_7",
            "channel-1",
        )
        consumer.accept.assert_awaited_once()

    async def test_receive_json_contesta_pong_y_notificacion_serializa_evento(self):
        consumer = NotificacionConsumer()
        consumer.send_json = AsyncMock()

        await consumer.receive_json({"type": "ping"})
        await consumer.notification_message(
            {
                "id": "n1",
                "notification_type": "conflicto_detectado",
                "title": "Conflicto",
                "message": "Aula ocupada",
                "unread_count": 3,
            }
        )

        consumer.send_json.assert_any_await({"type": "pong"})
        consumer.send_json.assert_any_await(
            {
                "id": "n1",
                "tipo": "notification",
                "type": "conflicto_detectado",
                "title": "Conflicto",
                "message": "Aula ocupada",
                "unread_count": 3,
            }
        )


class DisponibilidadAulaConsumerTests(IsolatedAsyncioTestCase):
    async def test_connect_accepta_y_disconnect_libera_grupo(self):
        consumer = DisponibilidadAulaConsumer()
        consumer.channel_layer = AsyncMock()
        consumer.channel_name = "channel-2"
        consumer.accept = AsyncMock()

        await consumer.connect()
        await consumer.disconnect(code=1000)

        consumer.channel_layer.group_add.assert_awaited_once_with(
            "disponibilidad_aulas",
            "channel-2",
        )
        consumer.channel_layer.group_discard.assert_awaited_once_with(
            "disponibilidad_aulas",
            "channel-2",
        )
        consumer.accept.assert_awaited_once()

    async def test_aula_actualizada_serializa_payload(self):
        consumer = DisponibilidadAulaConsumer()
        consumer.send_json = AsyncMock()

        await consumer.aula_actualizada({"aula_id": "a1", "disponible": True})

        consumer.send_json.assert_awaited_once_with(
            {
                "tipo": "aula_actualizada",
                "aula_id": "a1",
                "disponible": True,
            }
        )


class ProgresoAsignacionConsumerTests(IsolatedAsyncioTestCase):
    async def test_connect_rechaza_anonimo_y_acepta_autenticado(self):
        anon = ProgresoAsignacionConsumer()
        anon.scope = {"user": SimpleNamespace(is_authenticated=False)}
        anon.close = AsyncMock()

        await anon.connect()

        anon.close.assert_awaited_once_with(code=4401)

        consumer = ProgresoAsignacionConsumer()
        consumer.scope = {"user": SimpleNamespace(is_authenticated=True)}
        consumer.channel_layer = AsyncMock()
        consumer.channel_name = "channel-3"
        consumer.accept = AsyncMock()

        await consumer.connect()

        consumer.channel_layer.group_add.assert_awaited_once_with(
            "progreso_asignacion",
            "channel-3",
        )
        consumer.accept.assert_awaited_once()

    async def test_progreso_serializa_evento(self):
        consumer = ProgresoAsignacionConsumer()
        consumer.send_json = AsyncMock()

        await consumer.progreso({"porcentaje": 45, "grupos_procesados": 12})

        consumer.send_json.assert_awaited_once_with(
            {
                "tipo": "progreso",
                "porcentaje": 45,
                "grupos_procesados": 12,
            }
        )


class PanelSyncConsumerTests(IsolatedAsyncioTestCase):
    async def test_connect_rechaza_anonimo_y_acepta_autenticado(self):
        anon = PanelSyncConsumer()
        anon.scope = {"user": SimpleNamespace(is_authenticated=False)}
        anon.close = AsyncMock()

        await anon.connect()

        anon.close.assert_awaited_once_with(code=4401)

        consumer = PanelSyncConsumer()
        consumer.scope = {"user": SimpleNamespace(is_authenticated=True)}
        consumer.channel_layer = AsyncMock()
        consumer.channel_name = "channel-4"
        consumer.accept = AsyncMock()

        await consumer.connect()

        consumer.channel_layer.group_add.assert_awaited_once_with(
            "panel_sync",
            "channel-4",
        )
        consumer.accept.assert_awaited_once()

    async def test_catalogo_actualizado_serializa_evento(self):
        consumer = PanelSyncConsumer()
        consumer.send_json = AsyncMock()

        await consumer.catalogo_actualizado(
            {
                "entidad": "aulas",
                "accion": "actualizada",
                "detalle": "Aula sincronizada",
                "payload": {"aula_id": "a1"},
            }
        )

        consumer.send_json.assert_awaited_once_with(
            {
                "tipo": "catalogo_actualizado",
                "entidad": "aulas",
                "accion": "actualizada",
                "detalle": "Aula sincronizada",
                "payload": {"aula_id": "a1"},
            }
        )
