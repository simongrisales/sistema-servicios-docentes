# reservas/application/dtos.py
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass

@dataclass(frozen=True)
class CrearReservaInputDTO:
    """Datos de entrada para solicitar una reserva."""
    aula_id: str
    inicio: datetime
    fin: datetime
    solicitante_id: str

@dataclass(frozen=True)
class ConfirmarReservaInputDTO:
    """Dato de entrada para confirmar la reserva."""
    reserva_id: str

@dataclass(frozen=True)
class CancelarReservaInputDTO:
    """Dato de entrada para cancelar una reserva."""
    reserva_id: str

# DTOs de salida (pueden ser reutilizados o ampliados)
@dataclass(frozen=True)
class ReservaOutputDTO:
    """Representa los datos de la reserva después de un proceso exitoso."""
    reserva_id: str
    aula_id: str
    inicio: datetime
    fin: datetime
    solicitante_id: str
    estado: str

@dataclass(frozen=True)
class ConflictDTO:
    """Detalles sobre el conflicto detectado."""
    conflicto_reserva_id: str
    aula_id: str
    hora_inicio: datetime
    hora_fin: datetime