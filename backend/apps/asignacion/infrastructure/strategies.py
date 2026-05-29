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
        aulas_filtradas = [
            aula for aula in aulas
            if aula.get("disponible", True) and aula.get("activa", True)
        ]
        aulas_ordenadas = sorted(
            aulas_filtradas,
            key=lambda aula: aula.get("capacidad", 0),
        )
        ocupacion = set()
        asignaciones = []
        conflictos = []

        for grupo in grupos_ordenados:
            grupo_id = str(grupo.get("id") or grupo.get("grupo_id") or "")
            bloque_id = str(
                grupo.get("bloque_horario_id")
                or grupo.get("horario_bloque_id")
                or grupo.get("bloque_id")
                or ""
            )
            semestre = str(grupo.get("semestre") or "")
            estudiantes = grupo.get("num_estudiantes", 0)
            tipo_requerido = grupo.get("tipo_aula") or grupo.get("tipo") or None

            if not grupo_id or not bloque_id or not semestre:
                return ResultadoAsignacion(
                    exitoso=False,
                    mensaje="Hay grupos con datos incompletos para asignacion.",
                    conflicto_detalles=[grupo_id or "grupo_sin_id"],
                )

            aula = self._buscar_aula(
                aulas_ordenadas,
                estudiantes,
                bloque_id,
                ocupacion,
                tipo_requerido
            )
            if aula is None:
                # Si no encontramos con el tipo requerido, intentamos buscar sin la restricción de tipo como fallback
                if tipo_requerido:
                    aula = self._buscar_aula(
                        aulas_ordenadas,
                        estudiantes,
                        bloque_id,
                        ocupacion,
                        tipo_requerido=None
                    )
                
                if aula is None:
                    conflictos.append(f"Grupo {grupo_id} ({estudiantes} estudiantes) no encontro aula disponible en bloque {bloque_id}.")
                    continue

            aula_id = str(aula.get("id") or aula.get("aula_id"))
            ocupacion.add((aula_id, bloque_id))
            asignaciones.append(
                {
                    "grupo_id": grupo_id,
                    "aula_id": aula_id,
                    "bloque_horario_id": bloque_id,
                    "semestre": semestre,
                    "estado": "SIMULADO",
                }
            )

        if conflictos:
            return ResultadoAsignacion(
                exitoso=False,
                mensaje="No se pudo asignar aula a todos los grupos por conflictos de capacidad o disponibilidad.",
                conflicto_detalles=conflictos,
                asignaciones=asignaciones,
            )

        return ResultadoAsignacion(
            exitoso=True,
            mensaje="Simulacion de asignacion completada sin conflictos.",
            asignaciones=asignaciones,
        )

    @staticmethod
    def _buscar_aula(
        aulas: list[dict],
        estudiantes: int,
        bloque_id: str,
        ocupacion: set[tuple[str, str]],
        tipo_requerido: str | None = None,
    ) -> dict | None:
        for aula in aulas:
            aula_id = str(aula.get("id") or aula.get("aula_id"))
            if aula.get("capacidad", 0) < estudiantes:
                continue
            if (aula_id, bloque_id) in ocupacion:
                continue
            if tipo_requerido and aula.get("tipo") != tipo_requerido:
                continue
            return aula
        return None
