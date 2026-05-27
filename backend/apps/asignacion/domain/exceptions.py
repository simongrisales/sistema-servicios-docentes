from typing import Any

# Excepciones de negocio del módulo asignación
class AsignacionConflictoError(Exception):
    """Se lanza cuando se detectan conflictos irresolubles en la asignación."""
    def __init__(self, detalles: list[str], mensaje: str = "Asignación fallida debido a múltiples conflictos."):
        super().__init__(mensaje)
        self.detalles_conflicto = detalles

class CapacidadInsuficienteError(Exception):
    """Se lanza cuando el aula tiene capacidad menor al grupo."""
    pass

class SinAulasDisponiblesError(Exception):
    """Se lanza cuando no se encuentra ninguna aula que cumpla los criterios mínimos."""
    pass

class DatosIncompletosError(Exception):
    """Se lanza si faltan datos críticos de entrada para realizar la asignación (ej. Curso o Grupo)."""
    def __init__(self, mensaje: str = "Datos de entrada incompletos. Revisar grupo/curso/bloque horario."):
        super().__init__(mensaje)