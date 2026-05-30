from apps.notificaciones.domain.entities import TipoNotificacion


def test_tipos_de_notificacion_incluyen_los_canonicos():
    values = TipoNotificacion.values()

    assert TipoNotificacion.ASIGNACION_COMPLETADA in values
    assert TipoNotificacion.CONFLICTO_DETECTADO in values
    assert TipoNotificacion.RESERVA_CONFIRMADA in values
    assert TipoNotificacion.RESERVA_EXPIRADA in values
