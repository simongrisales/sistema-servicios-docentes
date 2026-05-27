from datetime import datetime
from typing import Optional

# Enum-like class for status management
class ReservaEstado:
    PENDIENTE = "pending"      # Solicitada, pendiente de validación o confirmación
    CONFIRMADA = "confirmed"  # Confirmada y bloquea el recurso en la fecha/hora
    CANCELADA = "cancelled"   # Cancelada por el solicitante
    EXPIRADA = "expired"      # Expiró automáticamente sin acción

class Reserva:
    """Representación de una reserva temporal de aula."""
    def __init__(self,
                 reserva_id: str,
                 aula_id: str,
                 bloque_horario_inicio: datetime,
                 bloque_horario_fin: datetime,
                 solicitante_id: str,
                 estado: str = ReservaEstado.PENDIENTE):
        self.reserva_id = reserva_id  # ID único de la reserva
        self.aula_id = aula_id        # ID del aula reservada (FK)
        self.bloque_horario_inicio = bloque_horario_inicio # Inicio en datetime
        self.bloque_horario_fin = bloque_horario_fin   # Fin en datetime
        self.solicitante_id = solicitante_id # ID del usuario que la solicita (FK)
        self.estado = estado

    def es_valida(self, current_date: datetime) -> bool:
        """Verifica si el objeto Reserva tiene un estado válido y no ha expirado."""
        return self.estado not in [ReservaEstado.CANCELADA] and self.bloque_horario_fin > current_date

    @staticmethod
    def crear(reserva_id: str, aula_id: str, inicio: datetime, fin: datetime, solicitante_id: str) -> 'Reserva':
        return Reserva(reserva_id, aula_id, inicio, fin, solicitante_id)

# Nota: Se pueden añadir más modelos de datos complejos aquí (ej. DatosDeConflictosDTO) si son necesarios en el dominio.