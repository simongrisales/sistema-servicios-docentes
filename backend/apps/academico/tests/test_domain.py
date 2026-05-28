from uuid import uuid4

import pytest

from ..domain.entities import Aula, TipoAula
from ..domain.exceptions import CapacidadAulaInvalidaError


def test_aula_creacion_valida():
    aula = Aula(
        id=uuid4(),
        nombre="Aula Magna",
        capacidad=300,
        tipo=TipoAula.AUDITORIO,
    )

    assert aula.capacidad == 300


def test_aula_rechaza_capacidad_invalida():
    with pytest.raises(CapacidadAulaInvalidaError):
        Aula(
            id=uuid4(),
            nombre="Aula sin capacidad",
            capacidad=0,
            tipo=TipoAula.AULA_REGULAR,
        )
