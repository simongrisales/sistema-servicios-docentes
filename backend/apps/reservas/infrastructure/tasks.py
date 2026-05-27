# reservas/infrastructure/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import ReservaModel

@shared_task(bind=True, max_retries=3)
def expiracion_automatica_reservas(self, modelo_reserva: ReservaModel):
    """
    Tarea Celery que se ejecuta periódicamente para buscar y cambiar el estado de reservas expiradas.
    Esta tarea debe ser llamada por un cronjob o worker dedicado.
    """
    try:
        if timezone.now() > modelo_reserva.fecha_expiracion and modelo_reserva.estado not in ['CANCELADA', 'CONFIRMADA']:
            print(f"Reserva {modelo_reserva.pk} expirada automáticamente.")
            # Actualizar el estado a EXPIRADO en la base de datos
            modelo_reserva.estado = 'expired'
            modelo_reserva.save()
            return True
        else:
            print(f"Reserva {modelo_reserva.pk} no requiere expiración.")
            return False
    except Exception as e:
        print(f"Error en la tarea de expiración: {e}")
        raise self.retry(exc=e, countdown=60)

# Nota importante: Esta tarea debe ser invocada periódicamente (ej., cada 15 minutos) desde un worker o cronjob externo para escanear modelos.