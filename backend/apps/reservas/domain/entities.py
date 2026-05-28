from dataclasses import dataclass
from datetime import datetime


class ReservaEstado:
    PENDIENTE = "pending"
    CONFIRMADA = "confirmed"
    CANCELADA = "cancelled"
    EXPIRADA = "expired"


@dataclass(frozen=True)
class Reserva:
    reserva_id: str
    aula_id: str
    bloque_horario_inicio: datetime
    bloque_horario_fin: datetime
    solicitante_id: str
    estado: str = ReservaEstado.PENDIENTE

    def es_valida(self, current_date: datetime) -> bool:
        return (
            self.estado not in {ReservaEstado.CANCELADA, ReservaEstado.EXPIRADA}
            and self.bloque_horario_fin > current_date
        )

    @classmethod
    def crear(
        cls,
        reserva_id: str,
        aula_id: str,
        inicio: datetime,
        fin: datetime,
        solicitante_id: str,
    ) -> "Reserva":
        return cls(reserva_id, aula_id, inicio, fin, solicitante_id)
