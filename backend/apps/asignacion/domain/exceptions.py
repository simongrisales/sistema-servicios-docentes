class AsignacionConflictoError(Exception):
    """Conflicto irresoluble durante la asignacion."""

    def __init__(
        self,
        detalles: list[str],
        mensaje: str = "Asignacion fallida por conflictos.",
    ) -> None:
        super().__init__(mensaje)
        self.detalles_conflicto = detalles


class CapacidadInsuficienteError(Exception):
    """El aula no tiene capacidad suficiente."""


class SinAulasDisponiblesError(Exception):
    """No existe un aula disponible para los criterios dados."""


class DatosIncompletosError(Exception):
    """Faltan datos criticos para ejecutar la asignacion."""
