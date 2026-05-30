from django.contrib.auth import get_user_model
from django.core.cache import cache

from apps.academico.infrastructure.models import HorarioBloqueModel
from apps.academico.infrastructure.repositories import AulaRepository, GrupoRepository
from apps.notificaciones.application.dtos import CrearNotificacionInputDTO
from apps.notificaciones.application.use_cases import NotificacionService
from apps.notificaciones.domain.entities import TipoNotificacion
from apps.notificaciones.infrastructure.repositories import NotificacionRepository

from ..domain.entities import Asignacion, ReglaAsignacion, ResultadoAsignacion
from ..domain.exceptions import (
    AsignacionConflictoError,
    CapacidadInsuficienteError,
    DatosIncompletosError,
)
from ..domain.interfaces import IAsignacionRepository, IAsignacionStrategy
from ..infrastructure.strategies import PrioridadEstudiantesStrategy
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
        notificacion_service: NotificacionService | None = None,
    ) -> None:
        self.asignacion_repo = asignacion_repo
        self.strategy = strategy
        self.notificacion_service = notificacion_service

    def validar_conflictos_horario(
        self,
        aula_id: str,
        bloque_horario_id: str,
        grupo_id: str,
        semestre: str,
    ) -> None:
        if self.asignacion_repo and self.asignacion_repo.existe_conflicto(
            aula_id,
            bloque_horario_id,
            semestre,
        ):
            raise AsignacionConflictoError(
                [
                    "El aula ya esta ocupada en ese bloque.",
                    f"Grupo afectado: {grupo_id}",
                ]
            )

    def ejecutar_asignacion_automatica(
        self, input_dto: AsignacionInputDTO
    ) -> AsignacionOutputDTO:
        self.validar_conflictos_horario(
            input_dto.aula_id,
            input_dto.bloque_horario_id,
            input_dto.grupo_id,
            input_dto.semestre,
        )
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

    def ejecutar_asignacion_automatica_semestre(
        self,
        semestre: str,
        grupos: list[dict] | None = None,
        aulas: list[dict] | None = None,
        reglas: list[ReglaAsignacion] | None = None,
    ) -> AsignacionOutputDTO:
        grupos_normalizados = grupos or self._obtener_grupos_semestre(semestre)
        aulas_normalizadas = aulas or self._obtener_aulas_disponibles()

        if not grupos_normalizados:
            raise DatosIncompletosError(
                f"No hay grupos cargados para el semestre {semestre}."
            )
        if not aulas_normalizadas:
            raise DatosIncompletosError(
                f"No hay aulas disponibles para el semestre {semestre}."
            )

        resultado = self._ejecutar_strategy(
            grupos_normalizados,
            aulas_normalizadas,
            reglas or [],
        )
        confirmadas = 0
        pendientes = 0

        for asignacion in resultado.asignaciones:
            if str(asignacion.get("estado", "")).upper() == "PENDIENTE":
                pendientes += 1
                continue

            aula_id = str(asignacion.get("aula_id") or "")
            bloque_id = str(asignacion.get("bloque_horario_id") or "")
            grupo_id = str(asignacion.get("grupo_id") or "")
            if not aula_id or not bloque_id or not grupo_id:
                pendientes += 1
                continue

            self.validar_conflictos_horario(aula_id, bloque_id, grupo_id, semestre)
            confirmadas += 1

            if self.asignacion_repo is not None:
                self.asignacion_repo.guardar(
                    Asignacion(
                        id=None,
                        grupo_id=grupo_id,
                        aula_id=aula_id,
                        bloque_horario_id=bloque_id,
                        semestre=semestre,
                        estado="CONFIRMADO",
                    )
                )

        self._invalidate_aulas_cache()
        self._publicar_notificacion_asignacion(
            semestre=semestre,
            total=len(resultado.asignaciones),
            pendientes=pendientes,
        )

        return AsignacionOutputDTO(
            grupo_id="",
            aula_id="",
            bloque_horario_id="",
            semestre=semestre,
            estado="RESUMEN",
            mensaje=resultado.mensaje,
            total_asignaciones=confirmadas,
            grupos_pendientes=pendientes,
            conflictos=resultado.conflicto_detalles,
            asignaciones=resultado.asignaciones,
        )

    def simular_asignacion(self, input_dto: SimulacionInputDTO) -> SimulacionOutputDTO:
        if self.strategy is None:
            return SimulacionOutputDTO(
                exitoso=True,
                mensaje="Simulacion preparada sin persistir datos.",
            )
        resultado = self._ejecutar_strategy(
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

    def _ejecutar_strategy(
        self,
        grupos: list[dict],
        aulas: list[dict],
        reglas: list[ReglaAsignacion],
    ) -> ResultadoAsignacion:
        strategy = self.strategy or PrioridadEstudiantesStrategy()
        return strategy.asignar(grupos, aulas, reglas)

    def _invalidate_aulas_cache(self) -> None:
        cache.delete("academico:aulas_disponibles")
        cache.delete("academico:aulas_disponibles_dto")

    def _publicar_notificacion_asignacion(
        self,
        semestre: str,
        total: int,
        pendientes: int,
    ) -> None:
        service = self.notificacion_service or NotificacionService(
            NotificacionRepository()
        )
        usuario = (
            get_user_model()
            .objects.filter(is_superuser=True)
            .order_by("id")
            .first()
        )
        if usuario is None:
            return

        service.enviar_notificacion(
            CrearNotificacionInputDTO(
                titulo="Asignacion de aulas completada",
                mensaje=(
                    f"El semestre {semestre} termino con {total} asignaciones y "
                    f"{pendientes} grupos pendientes."
                ),
                tipo_notificacion=TipoNotificacion.ASIGNACION_COMPLETADA,
                usuario_destino_id=str(usuario.pk),
            )
        )

    def _obtener_grupos_semestre(self, semestre: str) -> list[dict]:
        bloque_default = (
            HorarioBloqueModel.objects.filter(activo=True).values("id").first() or {}
        )
        bloque_id = str(bloque_default.get("id", ""))
        grupos = []
        for grupo in GrupoRepository().list_por_semestre(semestre):
            grupos.append(self._normalizar_grupo(grupo, bloque_id))
        return grupos

    def _obtener_aulas_disponibles(self) -> list[dict]:
        aulas = []
        for aula in AulaRepository().list_disponibles():
            aulas.append(self._normalizar_aula(aula))
        return aulas

    @staticmethod
    def _normalizar_grupo(grupo: object, bloque_id: str = "") -> dict:
        return {
            "id": str(getattr(grupo, "id", "")),
            "curso_id": str(getattr(grupo, "curso_id", "")),
            "docente_id": str(getattr(grupo, "docente_id", "")),
            "codigo": getattr(grupo, "codigo", ""),
            "num_estudiantes": getattr(grupo, "num_estudiantes", 0),
            "semestre": getattr(grupo, "semestre", ""),
            "bloque_horario_id": str(
                getattr(grupo, "bloque_horario_id", "") or bloque_id
            ),
            "tipo_aula": getattr(grupo, "tipo_aula", None),
            "activo": getattr(grupo, "activo", True),
        }

    @staticmethod
    def _normalizar_aula(aula: object) -> dict:
        return {
            "id": str(getattr(aula, "id", "")),
            "nombre": getattr(aula, "nombre", ""),
            "capacidad": getattr(aula, "capacidad", 0),
            "tipo": getattr(aula, "tipo", ""),
            "disponible": getattr(aula, "disponible", True),
            "activa": getattr(aula, "activa", True),
        }

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
ValidarConflictosHorario = AsignacionUseCaseService
