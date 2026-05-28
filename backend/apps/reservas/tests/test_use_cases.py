from datetime import datetime, timedelta

from ..application.dtos import CrearReservaInputDTO
from ..application.use_cases import ReservaService


def test_crear_reserva_sin_repositorio_devuelve_dto():
    service = ReservaService()
    output = service.crear_reserva(
        CrearReservaInputDTO(
            aula_id="a1",
            inicio=datetime.now(),
            fin=datetime.now() + timedelta(hours=1),
            solicitante_id="u1",
        )
    )

    assert output.aula_id == "a1"
