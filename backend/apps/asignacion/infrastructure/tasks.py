from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from apps.asignacion.application.use_cases import AsignacionUseCaseService
from apps.asignacion.domain.exceptions import (
    AsignacionConflictoError,
    DatosIncompletosError,
)
from apps.asignacion.infrastructure.repositories import AsignacionRepository
from apps.asignacion.infrastructure.strategies import PrioridadEstudiantesStrategy


@shared_task(bind=True, max_retries=3, name="asignacion.automatica")
def asignacion_automatica_task(self, semestre_id: str) -> dict[str, str]:
    servicio = AsignacionUseCaseService(
        asignacion_repo=AsignacionRepository(),
        strategy=PrioridadEstudiantesStrategy(),
    )
    try:
        resumen = servicio.ejecutar_asignacion_automatica_semestre(semestre_id)
        return {
            "semestre_id": semestre_id,
            "estado": "completada",
            "total_asignaciones": resumen.total_asignaciones,
            "grupos_pendientes": resumen.grupos_pendientes,
        }
    except (DatosIncompletosError, AsignacionConflictoError) as exc:
        return {
            "semestre_id": semestre_id,
            "estado": "fallida",
            "detalle": str(exc),
        }
    except Exception as exc:  # pragma: no cover - la tarea reporta el fallo
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc, countdown=2**self.request.retries) from exc
        return {
            "semestre_id": semestre_id,
            "estado": "fallida",
            "detalle": str(exc),
        }


@shared_task(name="asignacion.recalculo")
def recalculo_task(
    semestre_id: str | None = None,
    grupo_id: str | None = None,
) -> dict[str, str | None]:
    return {
        "estado": "programado",
        "semestre_id": semestre_id,
        "grupo_id": grupo_id,
    }


@shared_task(name="asignacion.masiva")
def asignacion_masiva_task(grupo_ids: list[int], semestre: str) -> dict:
    total = max(len(grupo_ids), 1)
    for index, _grupo_id in enumerate(grupo_ids, start=1):
        _publicar_progreso_asignacion(
            porcentaje=round(index * 100 / total),
            grupos_procesados=index,
        )
    return {
        "semestre": semestre,
        "total_procesados": len(grupo_ids),
        "resultados": [{"grupo_id": grupo_id} for grupo_id in grupo_ids],
    }


@shared_task(name="asignacion.recalculo_legacy")
def recalculo_automatico_task(
    grupo_id: str | None = None,
    semestre_id: str | None = None,
) -> dict[str, str | None]:
    return {
        "estado": "programado",
        "grupo_id": grupo_id,
        "semestre_id": semestre_id,
    }


def _publicar_progreso_asignacion(porcentaje: int, grupos_procesados: int) -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return
    try:
        async_to_sync(channel_layer.group_send)(
            "progreso_asignacion",
            {
                "type": "progreso",
                "porcentaje": porcentaje,
                "grupos_procesados": grupos_procesados,
            },
        )
    except Exception:
        return
