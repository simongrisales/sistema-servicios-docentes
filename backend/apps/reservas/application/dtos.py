from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrearReservaInputDTO:
    aula_id: str
    inicio: datetime
    fin: datetime
    solicitante_id: str


@dataclass(frozen=True)
class ConfirmarReservaInputDTO:
    reserva_id: str


@dataclass(frozen=True)
class CancelarReservaInputDTO:
    reserva_id: str


@dataclass(frozen=True)
class ReservaOutputDTO:
    reserva_id: str
    aula_id: str
    inicio: datetime
    fin: datetime
    solicitante_id: str
    estado: str
