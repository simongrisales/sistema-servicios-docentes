from django.conf import settings
from django.db import models

from apps.academico.infrastructure.models import AulaModel


class ReservaModel(models.Model):
    reserva_id = models.CharField(max_length=36, unique=True, db_index=True)
    aula = models.ForeignKey(
        AulaModel,
        on_delete=models.CASCADE,
        related_name="reservas",
    )
    inicio = models.DateTimeField(db_index=True)
    fin = models.DateTimeField(db_index=True)
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservas_solicitadas",
    )
    estado = models.CharField(max_length=30, default="pending")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reservas_reserva"
        indexes = [models.Index(fields=["aula", "inicio", "fin", "estado"])]
