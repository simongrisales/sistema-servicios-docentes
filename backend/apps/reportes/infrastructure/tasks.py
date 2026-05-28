from celery import shared_task

from .repositories import ReporteRepository


@shared_task(name="reportes.generar")
def generate_celery_report(reporte_id: int) -> None:
    repo = ReporteRepository()
    reporte = repo.get_reporte_by_id(reporte_id)
    if reporte is None:
        return
    repo.update_report_status(
        reporte_id,
        "COMPLETO",
        data={"mensaje": "Reporte generado asincronicamente."},
    )
