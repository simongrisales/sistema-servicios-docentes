from uuid import UUID

from ..domain.exceptions import CapacidadAulaInvalidaError, GrupoSinDocenteError
from ..domain.interfaces import IAulaRepository, IDocenteRepository, IGrupoRepository
from .dtos import (
    AulaInputDTO,
    AulaOutputDTO,
    CargaMasivaInputDTO,
    DocenteOutputDTO,
    GrupoInputDTO,
    GrupoOutputDTO,
)


class AcademicoService:
    """Casos de uso principales del modulo academico."""

    def __init__(
        self,
        aula_repo: IAulaRepository | None = None,
        grupo_repo: IGrupoRepository | None = None,
        docente_repo: IDocenteRepository | None = None,
    ) -> None:
        self.aula_repo = aula_repo
        self.grupo_repo = grupo_repo
        self.docente_repo = docente_repo

    def crear_aula(self, dto: AulaInputDTO) -> AulaOutputDTO:
        if dto.capacidad <= 0:
            raise CapacidadAulaInvalidaError(
                "La capacidad del aula debe ser mayor que cero."
            )
        return AulaOutputDTO(
            id=None,
            nombre=dto.nombre,
            capacidad=dto.capacidad,
            tipo=dto.tipo,
            disponible=dto.disponible,
        )

    def listar_aulas_disponibles(self) -> list[AulaOutputDTO]:
        if self.aula_repo is None:
            return []
        return [
            AulaOutputDTO(
                id=aula.id,
                nombre=aula.nombre,
                capacidad=aula.capacidad,
                tipo=str(aula.tipo),
                disponible=aula.disponible,
            )
            for aula in self.aula_repo.list_disponibles()
        ]

    def crear_grupo(self, dto: GrupoInputDTO) -> GrupoOutputDTO:
        if (
            self.docente_repo is not None
            and self.docente_repo.get(dto.docente_id) is None
        ):
            raise GrupoSinDocenteError("El grupo debe tener un docente valido.")
        return GrupoOutputDTO(
            id=None,
            curso_id=dto.curso_id,
            docente_id=dto.docente_id,
            codigo=dto.codigo,
            num_estudiantes=dto.num_estudiantes,
            semestre=dto.semestre,
        )

    def carga_masiva_grupos(self, dto: CargaMasivaInputDTO) -> list[GrupoOutputDTO]:
        return [self.crear_grupo(grupo) for grupo in dto.grupos]

    def obtener_docente(self, docente_id: UUID) -> DocenteOutputDTO | None:
        if self.docente_repo is None:
            return None
        docente = self.docente_repo.get(docente_id)
        if docente is None:
            return None
        return DocenteOutputDTO(
            id=docente.id,
            nombre=docente.nombre,
            email=docente.email,
        )


UseCasesService = AcademicoService
