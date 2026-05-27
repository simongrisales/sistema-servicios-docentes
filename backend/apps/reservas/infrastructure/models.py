# reservas/infrastructure/models.py

from django.db import models
from sistema_servicios_docentes.backend.apps.core.domain.entities import ReservaEstado # Asumiendo que la enums base están aquí o se importa el valor
from sistema_servicios_docentes.backend.apps.reservas.domain.interfaces import IReservaRepository

class ReservaModel(models.Model):
    """
    Modelo ORM para persistir una reserva temporal de aula.
    Se relaciona con Aula y HorarioBloque de la app academico/.
    """
    # Claves foráneas (FK) a modelos de academico/
    aula = models.ForeignKey('academico.infrastructure.models.AulaModel', on_delete=models.CASCADE, related_name='reservas')
    bloque_horario = models.ForeignKey('academico.infrastructure.models.HorarioBloqueModel', on_delete=models.CASCADE)
    solicitante = models.CharField(max_length=255) # Usuario/Sistema ID (FK a usuarios/usuarios.models)

    # Campos de Reserva
    estado = models.CharField(max_length=50, choices=[
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada')
    ], default='pending')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()

    class Meta:
        # Restricción de unicidad en el bloqueo para la misma aula/bloque horario,
        # pero esto debe ser manejado por lógica transaccional o unique constraint avanzado si es necesario.
        # Por simplicidad, asumimos que el modelo base lo maneja.
        unique_together = ('aula', 'bloque_horario')

    def __str__(self):
        return f"{self.get_estado_display()} - {self.aula.nombre} ({self.solicitante})"


# Nota: Se necesita un campo para el ID único de la reserva, ya que en el dominio se usa 'reserva_id'.
# Si usamos el primary key (pk) como identificador interno y lo exponemos vía API, no necesitamos otro campo.
# Para mantener el contrato del Dominio con "reserva_id", podríamos añadir un UUIDField o usar el pk.

# Se requiere que los modelos AulaModel y HorarioBloqueModel existan en academico/infrastructure/models.py