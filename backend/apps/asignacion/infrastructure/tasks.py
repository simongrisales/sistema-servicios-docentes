from celery import shared_task


@shared_task(name="asignacion.masiva")
def asignacion_masiva_task(grupo_ids: list[int], semestre: str) -> dict:
    return {
        "semestre": semestre,
        "total_procesados": len(grupo_ids),
        "resultados": [{"grupo_id": grupo_id} for grupo_id in grupo_ids],
    }


@shared_task(name="asignacion.recalculo")
def recalculo_automatico_task() -> dict[str, str]:
    return {"estado": "programado"}
