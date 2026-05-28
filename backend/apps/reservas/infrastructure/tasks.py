from celery import shared_task

from ..domain.entities import ReservaEstado
from .models import ReservaModel


@shared_task(name="reservas.expirar")
def expiracion_automatica_reservas() -> int:
    updated = ReservaModel.objects.filter(estado=ReservaEstado.PENDIENTE).update(
        estado=ReservaEstado.EXPIRADA
    )
    return updated
