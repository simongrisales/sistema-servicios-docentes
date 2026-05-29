from ..domain.entities import Asignacion, ResultadoAsignacion
from ..domain.exceptions import AsignacionConflictoError, CapacidadInsuficienteError
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
        from django.db import transaction

        with transaction.atomic():
            if self.asignacion_repo and self.asignacion_repo.existe_conflicto(
                input_dto.aula_id,
                input_dto.bloque_horario_id,
                input_dto.semestre,
            ):
                raise AsignacionConflictoError(["El aula ya esta ocupada en ese bloque."])

            self._validar_capacidad(input_dto)

            asignacion = Asignacion(
                id=None,
                grupo_id=str(input_dto.grupo_id),
                aula_id=str(input_dto.aula_id),
                bloque_horario_id=str(input_dto.bloque_horario_id),
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
            asignaciones=resultado.asignaciones,
        )

    def verificar_cobertura_total(self, semestre: str = "") -> CoberturaOutputDTO:
        if self.asignacion_repo is None or not semestre:
            return CoberturaOutputDTO(total_grupos=0, grupos_con_aula=0)
        return CoberturaOutputDTO(
            total_grupos=self.asignacion_repo.contar_grupos_por_semestre(semestre),
            grupos_con_aula=(
                self.asignacion_repo.contar_grupos_asignados_por_semestre(semestre)
            ),
        )

    def _validar_capacidad(self, input_dto: AsignacionInputDTO) -> None:
        if self.asignacion_repo is None:
            return
        obtener_grupo = getattr(self.asignacion_repo, "obtener_grupo", None)
        obtener_aula = getattr(self.asignacion_repo, "obtener_aula", None)
        if obtener_grupo is None or obtener_aula is None:
            return

        grupo = obtener_grupo(input_dto.grupo_id)
        aula = obtener_aula(input_dto.aula_id)
        if grupo and aula and aula.capacidad < grupo.num_estudiantes:
            raise CapacidadInsuficienteError(
                "El aula no tiene capacidad suficiente para el grupo."
            )


EjecutarAsignacionAutomatica = AsignacionUseCaseService
SimularAsignacion = AsignacionUseCaseService
