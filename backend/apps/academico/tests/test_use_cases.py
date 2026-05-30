from uuid import uuid4

import pytest

from ..application.dtos import (
    AulaInputDTO,
    CargaMasivaInputDTO,
    GrupoInputDTO,
)
from ..application.use_cases import AcademicoService
from ..domain.entities import Aula, Docente, Grupo, TipoAula
from ..domain.exceptions import CapacidadAulaInvalidaError, GrupoSinDocenteError


def test_crear_aula_devuelve_dto():
    output = AcademicoService().crear_aula(
        AulaInputDTO(nombre="Aula 101", capacidad=40, tipo="aula_regular")
    )

    assert output.nombre == "Aula 101"
    assert output.capacidad == 40


def test_crear_aula_sin_repo_conserva_datos_del_dto():
    output = AcademicoService().crear_aula(
        AulaInputDTO(nombre="Aula 303", capacidad=20, tipo="laboratorio")
    )

    assert output.id is None
    assert output.tipo == "laboratorio"


class FakeAulaRepository:
    def __init__(self) -> None:
        self.aula = Aula(
            id=uuid4(),
            nombre="Aula 202",
            capacidad=35,
            tipo=TipoAula.AULA_REGULAR,
        )

    def create(self, payload: dict):
        return Aula(
            id=uuid4(),
            nombre=payload["nombre"],
            capacidad=payload["capacidad"],
            tipo=TipoAula(payload["tipo"]),
            disponible=payload["disponible"],
        )

    def list_disponibles(self):
        return [self.aula]


class FakeGrupoRepository:
    def __init__(self) -> None:
        self.created = []

    def create(self, payload: dict):
        grupo = Grupo(
            id=uuid4(),
            curso_id=payload["curso_id"],
            docente_id=payload["docente_id"],
            codigo=payload["codigo"],
            num_estudiantes=payload["num_estudiantes"],
            semestre=payload["semestre"],
        )
        self.created.append(payload)
        return grupo


class FakeDocenteRepository:
    def __init__(self, exists: bool = True) -> None:
        self.exists = exists
        self.docente_id = uuid4()

    def get(self, docente_id):
        if not self.exists:
            return None
        return Docente(
            id=docente_id,
            nombre="Docente UCO",
            email="docente@uco.edu.co",
        )


def test_crear_aula_con_repo_y_capacidad_invalida():
    service = AcademicoService(aula_repo=FakeAulaRepository())

    output = service.crear_aula(
        AulaInputDTO(nombre="Aula 202", capacidad=35, tipo="aula_regular")
    )

    assert output.id is not None
    assert output.tipo == "aula_regular"

    with pytest.raises(CapacidadAulaInvalidaError):
        service.crear_aula(
            AulaInputDTO(nombre="Mala", capacidad=0, tipo="aula_regular")
        )


def test_listar_aulas_disponibles_usa_cache_y_repo(cache):
    service = AcademicoService(aula_repo=FakeAulaRepository())

    first = service.listar_aulas_disponibles()
    second = service.listar_aulas_disponibles()

    assert first[0].nombre == "Aula 202"
    assert second[0].nombre == "Aula 202"


@pytest.mark.django_db
def test_crear_grupo_y_carga_masiva_con_repo():
    curso_id = uuid4()
    docente_id = uuid4()
    grupo_repo = FakeGrupoRepository()
    service = AcademicoService(
        grupo_repo=grupo_repo,
        docente_repo=FakeDocenteRepository(),
    )
    dto = GrupoInputDTO(
        curso_id=curso_id,
        docente_id=docente_id,
        codigo="G1",
        num_estudiantes=25,
        semestre="2026-1",
    )

    output = service.crear_grupo(dto)
    lote = service.carga_masiva_grupos(CargaMasivaInputDTO(grupos=[dto]))

    assert output.codigo == "G1"
    assert lote[0].num_estudiantes == 25
    assert len(grupo_repo.created) == 2


@pytest.mark.django_db
def test_crear_grupo_sin_repo_y_carga_masiva_sin_repo():
    curso_id = uuid4()
    docente_id = uuid4()
    dto = GrupoInputDTO(
        curso_id=curso_id,
        docente_id=docente_id,
        codigo="G2",
        num_estudiantes=18,
        semestre="2026-1",
    )

    service = AcademicoService(docente_repo=FakeDocenteRepository())
    output = service.crear_grupo(dto)
    lote = service.carga_masiva_grupos(CargaMasivaInputDTO(grupos=[dto]))

    assert output.id is None
    assert output.codigo == "G2"
    assert lote[0].curso_id == curso_id


def test_crear_grupo_rechaza_docente_inexistente_y_obtener_docente():
    docente_id = uuid4()
    service = AcademicoService(docente_repo=FakeDocenteRepository(exists=False))

    with pytest.raises(GrupoSinDocenteError):
        service.crear_grupo(
            GrupoInputDTO(
                curso_id=uuid4(),
                docente_id=docente_id,
                codigo="G1",
                num_estudiantes=25,
                semestre="2026-1",
            )
        )

    assert service.obtener_docente(docente_id) is None
    docente = AcademicoService(docente_repo=FakeDocenteRepository()).obtener_docente(
        docente_id
    )
    assert docente.email == "docente@uco.edu.co"
