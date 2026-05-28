from ..domain.entities import Asignacion, ResultadoAsignacion
from ..domain.exceptions import AsignacionConflictoError
from ..domain.interfaces import IAsignacionRepository, IAsignacionStrategy
from .dtos import (
    AsignacionInputDTO,
    AsignacionOutputDTO,
    CoberturaOutputDTO,
    SimulacionInputDTO,
    SimulacionOutputDTO,
)


class AsignacionUseCaseService:
    """Orquesta asignacion automatica, simulacion y cobertura."""

    def __init__(
        self,
        asignacion_repo: IAsignacionRepository | None = None,
        strategy: IAsignacionStrategy | None = None,
    ) -> None:
        self.asignacion_repo = asignacion_repo
        self.strategy = strategy

    def ejecutar_asignacion_automatica(
        self, input_dto: AsignacionInputDTO
    ) -> AsignacionOutputDTO:
        if self.asignacion_repo and self.asignacion_repo.existe_conflicto(
            input_dto.aula_id,
            input_dto.bloque_horario_id,
            input_dto.semestre,
        ):
            raise AsignacionConflictoError(["El aula ya esta ocupada en ese bloque."])

        asignacion = Asignacion(
            id=0,
            grupo_id=int(input_dto.grupo_id),
            aula_id=int(input_dto.aula_id),
            bloque_horario_id=int(input_dto.bloque_horario_id),
            semestre=input_dto.semestre,
            estado="CONFIRMADO",
        )
        if self.asignacion_repo:
            asignacion = self.asignacion_repo.guardar(asignacion)
        return AsignacionOutputDTO(
            grupo_id=str(asignacion.grupo_id),
            aula_id=str(asignacion.aula_id),
            bloque_horario_id=str(asignacion.bloque_horario_id),
            semestre=asignacion.semestre,
            estado=asignacion.estado,
        )

    def simular_asignacion(self, input_dto: SimulacionInputDTO) -> SimulacionOutputDTO:
        if self.strategy is None:
            return SimulacionOutputDTO(
                exitoso=True,
                mensaje="Simulacion preparada sin persistir datos.",
            )
        resultado: ResultadoAsignacion = self.strategy.asignar(
            input_dto.grupos,
            input_dto.aulas,
            [],
        )
        return SimulacionOutputDTO(
            exitoso=resultado.exitoso,
            mensaje=resultado.mensaje,
            conflictos=resultado.conflicto_detalles,
        )

    def verificar_cobertura_total(self) -> CoberturaOutputDTO:
        return CoberturaOutputDTO(total_grupos=0, grupos_con_aula=0)


EjecutarAsignacionAutomatica = AsignacionUseCaseService
SimularAsignacion = AsignacionUseCaseService
