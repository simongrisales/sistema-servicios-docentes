from dataclasses import dataclass
from typing import List, Optional
from ..domain.entities import Grupo, Aula, HorarioBloque

@dataclass(frozen=True)
class AsignacionInputDTO:
    """Datos mínimos necesarios para intentar una asignación."""
    grupo_id: int
    bloque_horario: 'HorarioBloque' # Usar el objeto de dominio directamente
    semestre: str

@dataclass(frozen=True)
class SimulacionInputDTO:
    """Datos para ejecutar una simulación sin efectos en la DB."""
    grupo_id: int
    bloque_horario: 'HorarioBloque'
    semestre: str

@dataclass(frozen=True)
class CoberturaOutputDTO:
    """Resultado del proceso de validación de cobertura total."""
    grupos_con_aula: int
    total_grupos: int
    falta_porcentaje: float = 0.0