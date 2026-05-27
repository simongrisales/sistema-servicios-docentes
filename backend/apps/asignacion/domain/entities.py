from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(frozen=True)
class Asignacion:
    """Entidad de Dominio para una asignación confirmada de aula."""
    id: int
    grupo_id: int
    aula_id: int
    bloque_horario_id: int
    semestre: str
    estado: str # CONFIRMADA, RESERVADA

@dataclass(frozen=True)
class ReglaAsignacion:
    """Definición de una regla de negocio para el proceso de asignación."""
    nombre: str
    tipo: str # Ej: MIN_CAPACIDAD, MAX_DISTANCIA
    parametros: dict
    activa: bool = True

@dataclass(frozen=True)
class ResultadoAsignacion:
    """Contiene el resultado de un intento de asignación (éxito o conflicto)."""
    exitoso: bool
    mensaje: str
    aula_sugerida_id: Optional[int] = None
    conflicto_detalles: List[str] = field(default_factory=list)