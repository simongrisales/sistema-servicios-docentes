from datetime import datetime, timedelta

from ..domain.entities import Reserva, ReservaEstado


def test_reserva_valida_si_no_ha_expirado():
    reserva = Reserva(
        reserva_id="r1",
        aula_id="a1",
        bloque_horario_inicio=datetime.now(),
        bloque_horario_fin=datetime.now() + timedelta(hours=1),
        solicitante_id="u1",
        estado=ReservaEstado.PENDIENTE,
    )

    assert reserva.es_valida(datetime.now())
