from ..domain.entities import ReglaAsignacion, ResultadoAsignacion
from ..domain.interfaces import IAsignacionStrategy


class PrioridadEstudiantesStrategy(IAsignacionStrategy):
    """Asigna primero los grupos con mas estudiantes a aulas suficientes."""

    def asignar(
        self,
        grupos: list[dict],
        aulas: list[dict],
        reglas: list[ReglaAsignacion],
    ) -> ResultadoAsignacion:
        del reglas
        grupos_ordenados = sorted(
            grupos,
            key=lambda grupo: grupo.get("num_estudiantes", 0),
            reverse=True,
        )
        for grupo in grupos_ordenados:
            estudiantes = grupo.get("num_estudiantes", 0)
            aula = next(
                (
                    candidata
                    for candidata in aulas
                    if candidata.get("capacidad", 0) >= estudiantes
                ),
                None,
            )
            if aula is None:
                return ResultadoAsignacion(
                    exitoso=False,
                    mensaje="No hay aula con capacidad suficiente.",
                    conflicto_detalles=[str(grupo.get("id"))],
                )
        return ResultadoAsignacion(
            exitoso=True,
            mensaje="Simulacion de asignacion completada.",
        )
