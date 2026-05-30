from celery import shared_task
from django.db import transaction
from django.utils import timezone

from ..domain.entities import ReservaEstado
from .models import ReservaModel


@shared_task(name="reservas.expirar")
def expiracion_automatica_reservas() -> int:
    with transaction.atomic():
        updated = (
            ReservaModel.objects.select_for_update()
            .filter(estado=ReservaEstado.PENDIENTE, fin__lt=timezone.now())
            .update(estado=ReservaEstado.EXPIRADA)
        )
    return updated
