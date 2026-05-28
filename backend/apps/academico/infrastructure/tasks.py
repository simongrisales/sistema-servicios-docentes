from celery import shared_task


@shared_task(name="academico.carga_masiva_grupos")
def carga_masiva_grupos_task(total_registros: int) -> dict[str, int]:
    """Tarea de marcador para procesar cargas masivas academicas."""

    return {"registros_recibidos": total_registros}
