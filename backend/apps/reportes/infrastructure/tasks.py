# reportes/application/tasks.py

from celery import shared_task
from datetime import date
from backend.apps.reportes.domain.interfaces import IReporteGenerador
from backend.apps.reportes.infrastructure.repositories import ReporteRepository

@shared_task(bind=True, name='generate_celery_report')
def generate_celery_report(self, reporte_id: int):
    """
    Tarea Celery que contiene la lógica de negocio pesada para generar reportes.
    Esta tarea se invoca cuando un usuario solicita un reporte asíncrono.

    Args:
        reporte_id (int): ID del registro en ReporteModel a actualizar al finalizar.
    """
    # Inicializar el repositorio dentro de la tarea para acceder al contexto de DB
    repo = ReporteRepository()

    try:
        # 1. Obtener la entidad base y sus parámetros
        reporte_entidad = repo.get_reporte_by_id(reporte_id)
        if not reporte_entidad:
            raise ValueError("Reporte ID no encontrado.")

        # 2. Aquí se debería decidir qué generador usar basado en el tipo de reporte (Strategy Pattern implícito)
        # Ejemplo: Si es Ocupación, usar GeneracionOcupacionStrategy()
        print(f"--- Iniciando generación reportes para {reporte_entidad.titulo} ---")

        # 3. EJECUTAR LÓGICA PESADA AQUÍ (Ejemplo de simulación)
        # Simulamos que el proceso tardó y generó datos exitosos.
        data_generada = {
            "total_registros": 500,
            "detalles_por_periodo": [
                {"mes": "Mayo", "ocupacion_pct": 0.85},
                {"mes": "Junio", "ocupacion_pct": 0.72}
            ],
            "metrica_clave": "Alta utilización en periodos críticos."
        }

        # 4. Actualizar el estado a COMPLETO y guardar los datos raw
        repo.update_report_status(reporte_id, 'COMPLETO', data=data_generada)
        print("--- Reporte generado y DB actualizado exitosamente ---")


    except Exception as e:
        # 5. En caso de error, actualizar el estado a FALLIDO
        import logging
        logging.error(f"ERROR FATAL en la generación del reporte {reporte_id}: {str(e)}")

        repo.update_report_status(reporte_id, 'FALLIDO', data={"error": str(e)})