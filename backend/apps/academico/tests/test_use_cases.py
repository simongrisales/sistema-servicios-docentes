from ..application.dtos import AulaInputDTO
from ..application.use_cases import AcademicoService


def test_crear_aula_devuelve_dto():
    output = AcademicoService().crear_aula(
        AulaInputDTO(nombre="Aula 101", capacidad=40, tipo="aula_regular")
    )

    assert output.nombre == "Aula 101"
    assert output.capacidad == 40
